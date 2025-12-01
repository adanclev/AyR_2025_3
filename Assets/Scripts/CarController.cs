using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarController : MonoBehaviour
{
    public TrackPath track; // Arrastra tu GameObject "TrackPath" aquí en el Inspector

    // --- PID 1: Dirección ---
    public PIDController steeringPid = new PIDController();
    public float maxSteeringAngle = 45f; // Grados máximos de giro

    // --- PID 2: Velocidad ---
    public PIDController speedPid = new PIDController();
    public float maxSpeed = 10f;  // Velocidad normal
    public float minSpeed = 3f;   // Velocidad al desacelerar (¡nunca 0!)
    public float detectionDistance = 5f; // Qué tan lejos "ve" el coche
    public LayerMask obstacleLayer; // Configura una Layer "Obstacle" para la persona

    private Rigidbody2D rb;
    private float currentSpeed = 0f;

    // --- VARIABLES PARA RESPAWN ---
    private Vector3 startPosition;
    private Quaternion startRotation;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        steeringPid.Reset();
        speedPid.Reset();
    }

    void FixedUpdate()
    {
        // --- LÓGICA DE VELOCIDAD (PID 2) ---

        // 1. ¿Cuál es nuestra velocidad objetivo?
        float targetSpeed = GetTargetSpeed();

        // 2. ¿Cuál es nuestra velocidad actual?
        // Usamos la magnitud de la velocidad en la dirección "hacia adelante" del coche
        float currentForwardSpeed = Vector2.Dot(rb.velocity, transform.up);

        // 3. Calcular la fuerza del motor/freno con el PID 2
        // El setpoint es la velocidad que QUEREMOS, la measurement es la que TENEMOS.
        float force = speedPid.Calculate(targetSpeed, currentForwardSpeed);

        // 4. Aplicar la fuerza
        rb.AddForce(transform.up * force);
        currentSpeed = rb.velocity.magnitude; // Guardar para el giro


        // --- LÓGICA DE DIRECCIÓN (PID 1) ---

        // 1. Calcular el Error de Desvío Lateral (CTE)
        Vector3 closestPoint = track.GetClosestPointOnPath(transform.position);
        float cte = CalculateCTE(closestPoint);

        // 2. Calcular el ángulo de giro con el PID 1
        // El setpoint es 0 (queremos estar en el centro), la measurement es el CTE.
        float steerOutput = steeringPid.Calculate(0, cte);
        float steeringAngle = Mathf.Clamp(steerOutput, -maxSteeringAngle, maxSteeringAngle);

        // 3. Aplicar el giro (Rotación)
        // Solo giramos si nos estamos moviendo
        if (currentSpeed > 0.1f)
        {
            // El ángulo de giro se convierte en torque (fuerza de rotación)
            rb.AddTorque(-steeringAngle * Time.fixedDeltaTime * (currentSpeed / maxSpeed));
        }
    }

    float GetTargetSpeed()
    {
        // Lanzar un rayo (sensor) hacia adelante
        RaycastHit2D hit = Physics2D.Raycast(transform.position, transform.up, detectionDistance, obstacleLayer);

        if (hit.collider != null)
        {
            // ¡Obstáculo detectado! Bajar la velocidad objetivo.
            // (Tu profesor quiere ver esto)
            return minSpeed;
        }
        else
        {
            // Sin obstáculo. Volver a la velocidad máxima.
            return maxSpeed;
        }
    }

    float CalculateCTE(Vector3 closestPoint)
    {
        // Calcular la distancia
        float distance = Vector3.Distance(transform.position, closestPoint);

        // Calcular de qué lado estamos (izq/der)
        Vector3 directionToPoint = (closestPoint - transform.position).normalized;
        float side = Vector3.Dot(transform.right, directionToPoint);

        // Si side es > 0, el punto está a la derecha (+).
        // Si side es < 0, el punto está a la izquierda (-).
        return distance * Mathf.Sign(side);
    }
}
