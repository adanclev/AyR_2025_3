using UnityEngine;
using UnityEngine.InputSystem; // Necesario para InputAction.CallbackContext

public class CarController : MonoBehaviour
{
    // Parámetros configurables
    [SerializeField] private float dragFactor = 0.95f;
    [SerializeField] private float accelerationFactor = 30.0f;
    [SerializeField] private float turnFactor = 3.5f;
    [SerializeField] private float maxSpeed = 20f;
    [SerializeField] private string trackZoneTag = "TrackZone";
    
    // Parámetros para el giro asistido
    [Header("Asistencia de Giro")]
    [SerializeField] private float assistedAcceleration = 0.6f; // Aceleración extra cuando solo se gira
    [SerializeField] private float assistedTurnMultiplier = 2.0f; // Factor para hacer el giro más cerrado/derrape

    // Estado interno
    private float rotationAngle = 0f;
    private float velocityVsUp = 0f;
    private bool isAccelerating = false;             // NUEVO: Estado de aceleración automática
    private bool isBrakingOrReversing = false;     // NUEVO: Estado de Reversa/Freno automático

    // Componentes
    private Rigidbody2D carRb2D;
    private CarInputHandler inputHandler;

    private void Awake()
    {
        carRb2D = GetComponent<Rigidbody2D>();
        inputHandler = GetComponent<CarInputHandler>();
    }

    private void FixedUpdate()
    {
        ApplyEngineForce();
        KillOrthogonalVelocity();
        ApplySteering();
    }

    // --- MÉTODOS DE TOGGLE PARA EL INPUT ---

    /// <summary>
    /// Alterna el estado de aceleración automática con un solo toque.
    /// </summary>
    public void ToggleAcceleration(InputAction.CallbackContext context)
    {
        if (context.started)
        {
            isAccelerating = !isAccelerating;
            // Si activamos la aceleración, desactivamos el freno para evitar conflicto
            if (isAccelerating)
            {
                isBrakingOrReversing = false;
            }
            Debug.Log($"Aceleración automática: {isAccelerating}");
        }
    }
    
    /// <summary>
    /// Alterna el estado de reversa/freno automático con un solo toque.
    /// </summary>
    public void ToggleBrake(InputAction.CallbackContext context)
    {
        if (context.started)
        {
            isBrakingOrReversing = !isBrakingOrReversing;
            // Si activamos el freno, desactivamos la aceleración para evitar conflicto
            if (isBrakingOrReversing)
            {
                isAccelerating = false;
            }
            Debug.Log($"Freno/Reversa automática: {isBrakingOrReversing}");
        }
    }
    
    // ------------------------------------------

    /// <summary>
    /// Aplica la fuerza del motor, usando los estados de toggle.
    /// </summary>
    private void ApplyEngineForce()
    {
        velocityVsUp = Vector2.Dot(transform.up, carRb2D.linearVelocity);

        // Limitar velocidad si está acelerando (automáticamente)
        if (velocityVsUp > maxSpeed && isAccelerating) return;
        if (velocityVsUp < -maxSpeed * 0.5f && isBrakingOrReversing) return;
        if (carRb2D.linearVelocity.sqrMagnitude > maxSpeed * maxSpeed && isAccelerating) return;

        // 🚨 CÁLCULO DE FUERZA FINAL
        float throttleInput = 0f;

        if (isBrakingOrReversing)
        {
            throttleInput = -1f; // Aplicar reversa/freno total
        }
        else if (isAccelerating)
        {
            throttleInput = 1f; // Aplicar aceleración total
        }
        
        float finalThrottle = throttleInput;

        // Bandera para saber si estamos usando la aceleración asistida
        bool isAssistedTurning = false;

        // Giro asistido: Solo si NO hay aceleración o freno activos Y se está girando
        if (!isAccelerating && !isBrakingOrReversing && !Mathf.Approximately(inputHandler.move.x, 0f))
        {
            if (velocityVsUp < maxSpeed * 0.75f) 
            {
                finalThrottle = assistedAcceleration;
                isAssistedTurning = true;
            }
        }
        
        // Aplicación del Drag (Frenado pasivo): Solo si no hay fuerza activa ni asistencia
        if (Mathf.Approximately(finalThrottle, 0f) && !isAssistedTurning)
        {
            // Aplicar fricción pasiva para detener el coche
            carRb2D.linearDamping = Mathf.Lerp(carRb2D.linearDamping, 3.0f, Time.fixedDeltaTime * 3);
        }
        else
        {
            // Eliminar fricción pasiva si hay movimiento activo
            carRb2D.linearDamping = 0f;
        }

        // Vector de fuerza del motor
        Vector2 engineForceVector = transform.up * finalThrottle * accelerationFactor;

        // Aplicar fuerza
        carRb2D.AddForce(engineForceVector, ForceMode2D.Force);
    }

    /// <summary>
    /// Aplica el giro del vehículo.
    /// </summary>
    private void ApplySteering()
    {
        float speed = carRb2D.linearVelocity.magnitude;
        float turnMultiplier = speed < 0.1f ? 0.3f : Mathf.Clamp01(speed / 8f);

        // Giro más cerrado/asistido (solo si NO hay aceleración manual y SOLO se está girando)
        // Nota: Como 'inputHandler.move.y' ahora siempre es 0, solo comprobamos el giro.
        if (!Mathf.Approximately(inputHandler.move.x, 0f))
        {
            // Si no hay aceleración o freno activos (el giro asistido es más cerrado)
            if (!isAccelerating && !isBrakingOrReversing)
            {
                 turnMultiplier *= assistedTurnMultiplier;
            }
        }

        // Determinar dirección según movimiento (para invertir la dirección del giro en reversa)
        float direction = Vector2.Dot(carRb2D.linearVelocity, transform.up) >= 0 ? 1f : -1f;

        // Ajustar ángulo de rotación
        rotationAngle -= inputHandler.move.x * turnFactor * turnMultiplier * direction;

        carRb2D.MoveRotation(rotationAngle);
    }

    /// <summary>
    /// Elimina la velocidad ortogonal para evitar derrapes irreales.
    /// </summary>
    private void KillOrthogonalVelocity()
    {
        Vector2 forwardVelocity = transform.up * Vector2.Dot(carRb2D.linearVelocity, transform.up);
        carRb2D.linearVelocity = forwardVelocity;
    }

    // --- Lógica de Juego (sin cambios) ---
    private void OnTriggerExit2D(Collider2D other)
    {
        if (other.CompareTag(trackZoneTag))
        {
            Debug.Log("Saliste de la pista. ¡Juego terminado!");
            GameOver();
        }
    }

    private void GameOver()
    {
        carRb2D.linearVelocity = Vector2.zero;
        carRb2D.angularVelocity = 0f;
        enabled = false;
    }
}