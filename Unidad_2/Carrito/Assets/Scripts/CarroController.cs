using UnityEngine;
using UnityEngine.InputSystem;
using System.Collections; // 🚨 NECESARIO para usar Corutinas (IEnumerator)

public class CarroController : MonoBehaviour // CLASE PRINCIPAL
{
    // Parámetros configurables
    [SerializeField] private float accelerationFactor = 30.0f;
    [SerializeField] private float turnFactor = 3.5f;
    [SerializeField] private float maxSpeed = 20f;
    [SerializeField] private string trackZoneTag = "TrackZone"; // Tag usado para detectar el límite

    // 🚨 NUEVA VARIABLE: Tiempo para ignorar los límites al inicio
    [SerializeField] private float startGracePeriod = 0.5f;

    // Parámetros para el giro asistido
    [Header("Asistencia de Giro")]
    [SerializeField] private float assistedAcceleration = 0.6f;
    [SerializeField] private float assistedTurnMultiplier = 2.0f;

    // Estado interno
    private float rotationAngle = 0f;
    private float velocityVsUp = 0f;
    private bool isAccelerating = false;
    private bool isBrakingOrReversing = false;
    public bool IsCarReversing => isBrakingOrReversing;

    // Componentes
    private Rigidbody2D carRb2D;
    private CarroInputHandler inputHandler;

    private void Awake()
    {
        carRb2D = GetComponent<Rigidbody2D>();
        inputHandler = GetComponent<CarroInputHandler>();
        rotationAngle = transform.eulerAngles.z;
    }

    private void Start()
    {
        // Detiene el coche, resetea el estado y garantiza que no haya velocidad inicial
        carRb2D.linearVelocity = Vector2.zero;
        carRb2D.angularVelocity = 0f;
        isAccelerating = false;

        // 🚨 INICIA LA CORUTINA: Desactiva los límites por 0.5 segundos
        StartCoroutine(ToggleBoundaryColliders(false, startGracePeriod));
    }

    private void FixedUpdate()
    {
        ApplyEngineForce();
        KillOrthogonalVelocity();
        ApplySteering();
    }

    // --- MÉTODOS DE TOGGLE Y LÓGICA DE MOVIMIENTO (Sin cambios) ---

    public void ToggleAcceleration(InputAction.CallbackContext context)
    {
        if (context.started)
        {
            isAccelerating = !isAccelerating;
            if (isAccelerating)
            {
                isBrakingOrReversing = false;
            }
            Debug.Log($"Aceleración automática: {isAccelerating}");
        }
    }

    public void ToggleBrake(InputAction.CallbackContext context)
    {
        if (context.started)
        {
            isBrakingOrReversing = !isBrakingOrReversing;
            if (isBrakingOrReversing)
            {
                isAccelerating = false;
            }
            Debug.Log($"Freno/Reversa automática: {isBrakingOrReversing}");
        }
    }

    private void ApplyEngineForce()
    {
        velocityVsUp = Vector2.Dot(transform.up, carRb2D.linearVelocity);
        if (velocityVsUp > maxSpeed && isAccelerating) return;
        if (velocityVsUp < -maxSpeed * 0.5f && isBrakingOrReversing) return;
        if (carRb2D.linearVelocity.sqrMagnitude > maxSpeed * maxSpeed && isAccelerating) return;

        float throttleInput = 0f;
        if (isBrakingOrReversing) { throttleInput = -1f; }
        else if (isAccelerating) { throttleInput = 1f; }

        float finalThrottle = throttleInput;
        bool isAssistedTurning = false;

        if (!isAccelerating && !isBrakingOrReversing && !Mathf.Approximately(inputHandler.move.x, 0f))
        {
            if (velocityVsUp < maxSpeed * 0.75f)
            {
                finalThrottle = assistedAcceleration;
                isAssistedTurning = true;
            }
        }

        if (Mathf.Approximately(finalThrottle, 0f) && !isAssistedTurning)
        {
            carRb2D.linearDamping = Mathf.Lerp(carRb2D.linearDamping, 3.0f, Time.fixedDeltaTime * 3);
        }
        else
        {
            carRb2D.linearDamping = 0f;
        }

        Vector2 engineForceVector = transform.up * finalThrottle * accelerationFactor;
        carRb2D.AddForce(engineForceVector, ForceMode2D.Force);
    }

    private void ApplySteering()
    {
        float speed = carRb2D.linearVelocity.magnitude;
        float turnMultiplier = speed < 0.1f ? 0.3f : Mathf.Clamp01(speed / 8f);

        if (!Mathf.Approximately(inputHandler.move.x, 0f))
        {
            if (!isAccelerating && !isBrakingOrReversing)
            {
                turnMultiplier *= assistedTurnMultiplier;
            }
        }

        float direction = Vector2.Dot(carRb2D.linearVelocity, transform.up) >= 0 ? 1f : -1f;
        rotationAngle -= inputHandler.move.x * turnFactor * turnMultiplier * direction;
        carRb2D.MoveRotation(rotationAngle);
    }

    private void KillOrthogonalVelocity()
    {
        Vector2 forwardVelocity = transform.up * Vector2.Dot(carRb2D.linearVelocity, transform.up);
        carRb2D.linearVelocity = forwardVelocity;
    }

    // ------------------------------------------

    // 🚨 CORUTINA: Desactiva los colliders de límite para evitar la detección al inicio
    private IEnumerator ToggleBoundaryColliders(bool enable, float delay)
    {
        // 1. Encuentra los límites
        GameObject[] boundaryZones = GameObject.FindGameObjectsWithTag(trackZoneTag);

        // 2. Deshabilita los colliders inmediatamente
        foreach (GameObject zone in boundaryZones)
        {
            Collider2D col = zone.GetComponent<Collider2D>();
            if (col != null)
            {
                col.enabled = false;
            }
        }

        yield return new WaitForSeconds(delay); // 3. Espera el tiempo de gracia

        // 4. Vuelve a habilitar los colliders después del tiempo de gracia
        foreach (GameObject zone in boundaryZones)
        {
            Collider2D col = zone.GetComponent<Collider2D>();
            if (col != null)
            {
                col.enabled = true;
            }
        }
    }

    // --- LÓGICA DE JUEGO (SENSOR/TRIGGER) ---

    /// <summary>
    /// Detecta la entrada al sensor de límite. Requiere que el límite tenga Is Trigger MARCADo.
    /// </summary>
    private void OnTriggerEnter2D(Collider2D other)
    {
        // Verifica si entramos en el área del límite (TrackZone)
        if (other.CompareTag(trackZoneTag))
        {
            Debug.Log("¡Límite detectado por sensor! Juego terminado.");
            GameOver();
        }
    }

    // --- Lógica de Fin de Juego ---

    private void GameOver()
    {
        carRb2D.linearVelocity = Vector2.zero;
        carRb2D.angularVelocity = 0f;
        enabled = false;
    }

    public void StopCarOnWin()
    {
        carRb2D.linearVelocity = Vector2.zero;
        carRb2D.angularVelocity = 0f;
        enabled = false;
    }
}