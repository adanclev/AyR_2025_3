using UnityEngine;
using UnityEngine.InputSystem;

public class CarInputHandler : MonoBehaviour
{
    private CarController carController; // Referencia al componente CarController
    private InputAction m_MoveAction;
    private Vector2 _move;

    private void Awake()
    {
        carController = GetComponent<CarController>();
        if (carController == null)
        {
            Debug.LogError("CarInputHandler requiere un CarController en el mismo GameObject.");
            enabled = false;
            return;
        }

        m_MoveAction = InputSystem.actions.FindAction("Player/Move");
        m_MoveAction.Enable();

        // 🚨 CONEXIÓN CLAVE: Toggle de Aceleración (valor Y positivo)
        m_MoveAction.started += context => {
            // Solo llamar a ToggleAcceleration si la entrada vertical es positiva (Acelerar: W o Flecha Arriba)
            if (context.ReadValue<Vector2>().y > 0.5f)
            {
                carController.ToggleAcceleration(context);
            }
        };

        // 🚨 CONEXIÓN CLAVE: Toggle de Reversa/Freno (valor Y negativo)
        m_MoveAction.started += context => {
            // Solo llamar a ToggleBrake si la entrada vertical es negativa (Frenar: S o Flecha Abajo)
            if (context.ReadValue<Vector2>().y < -0.5f)
            {
                carController.ToggleBrake(context);
            }
        };
    }

    public Vector2 move { get { return _move; } }

    private void Update()
    {
        // 1. Leemos el valor del Vector2 completo
        Vector2 rawMove = m_MoveAction.ReadValue<Vector2>();

        // 2. Filtramos la entrada:
        // El eje Y (aceleración/freno) ahora se maneja por estados booleanos en CarController.
        // Aquí solo necesitamos el valor X (giro) y el Y debe ser 0.
        _move = new Vector2(rawMove.x, 0f); 
    }
}