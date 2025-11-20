using UnityEngine;
using UnityEngine.InputSystem;

public class CarroInputHandler : MonoBehaviour // <-- CORRECCIÓN CLAVE: Hereda de MonoBehaviour
{
    private CarroController carController; // <-- Referencia al Carro Controller
    private InputAction m_MoveAction;
    private Vector2 _move;

    private void Awake()
    {
        // Busca el componente de control
        carController = GetComponent<CarroController>();

        if (carController == null)
        {
            // Mensaje de error personalizado, ahora preciso
            Debug.LogError("El script CarroInputHandler requiere un CarroController en el mismo GameObject.");
            enabled = false;
            return;
        }

        m_MoveAction = InputSystem.actions.FindAction("Player/Move");
        m_MoveAction.Enable();

        // Conexiones de Input (Toggles)
        m_MoveAction.started += context => {
            if (context.ReadValue<Vector2>().y > 0.5f)
            {
                carController.ToggleAcceleration(context);
            }
        };

        m_MoveAction.started += context => {
            if (context.ReadValue<Vector2>().y < -0.5f)
            {
                carController.ToggleBrake(context);
            }
        };
    }

    public Vector2 move { get { return _move; } }

    private void Update()
    {
        Vector2 rawMove = m_MoveAction.ReadValue<Vector2>();
        _move = new Vector2(rawMove.x, 0f); // Solo propagamos el giro (X)
    }
}