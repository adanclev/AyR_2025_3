using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarControllerSimple : MonoBehaviour
{
    [Header("Configuración de la Pista")]
    public TrackPath track;
    public float radioX = 10f;
    public float radioY = 5f;

    [Header("Configuración del Coche")]
    public float motorSpeed = 20f; // Velocidad Máxima
    public float acceleration = 10f; // Qué tan rápido acelera/frena
    public float rotationSpeed = 300f; // Velocidad de giro (importante si vas rápido)

    [Header("PIDs")]
    // Kp=3, Ki=0, Kd=0.5 funcionan bien
    public PIDController steeringPid = new PIDController();

    [Header("Sensores")]
    public float detectionDistance = 4f;
    public LayerMask obstacleLayer;

    // Variable privada para guardar la velocidad real
    private float currentSpeed = 0f;

    void Start()
    {
        PlaceCarOnTrack();
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.R)) PlaceCarOnTrack();

        // --- 1. VELOCIDAD Y OBSTÁCULOS ---
        float targetSpeed = motorSpeed;
        RaycastHit2D hit = Physics2D.Raycast(transform.position, transform.up, detectionDistance, obstacleLayer);

        if (hit.collider != null) targetSpeed = 0f;

        // Esto permite que la velocidad se mantenga y aumente correctamente
        currentSpeed = Mathf.MoveTowards(currentSpeed, targetSpeed, acceleration * Time.deltaTime);

        // Mover el coche
        transform.Translate(Vector3.up * currentSpeed * Time.deltaTime);


        // --- 2. LÓGICA PID (DIRECCIÓN) ---
        if (track != null)
        {
            Vector3 closestPoint = track.GetClosestPointOnPath(transform.position);
            float cte = CalculateCTE(closestPoint);

            // Debug visual
            Debug.DrawLine(transform.position, closestPoint, Color.green);

            // PID
            float pidOutput = steeringPid.Calculate(0, cte);

            // Aplicar giro
            float rotationAmount = pidOutput * rotationSpeed * Time.deltaTime;
            transform.Rotate(0, 0, rotationAmount);
        }
    }

    public void PlaceCarOnTrack()
    {
        float randomAngle = Random.Range(0f, 360f) * Mathf.Deg2Rad;
        float x = Mathf.Cos(randomAngle) * radioX;
        float y = Mathf.Sin(randomAngle) * radioY;
        transform.position = new Vector3(x, y, 0);

        // Alinear
        float nextAngle = randomAngle + 0.1f;
        Vector3 lookDir = (new Vector3(Mathf.Cos(nextAngle) * radioX, Mathf.Sin(nextAngle) * radioY, 0) - transform.position).normalized;
        transform.up = lookDir;

        steeringPid.Reset();
        currentSpeed = motorSpeed; // Arrancar con velocidad
    }

    float CalculateCTE(Vector3 closestPoint)
    {
        float distance = Vector3.Distance(transform.position, closestPoint);
        Vector3 directionToPoint = (closestPoint - transform.position).normalized;
        float side = Vector3.Dot(transform.right, directionToPoint);
        return distance * Mathf.Sign(side);
    }
}
