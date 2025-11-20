using UnityEngine;
using TMPro;
using System;
using System.Collections;

public class LapCounter : MonoBehaviour
{
    // Variables públicas para configurar en el Inspector
    public TextMeshProUGUI lapText;
    public int targetLaps = 2; // Vueltas a completar
    public string playerTag = "Player";

    [Header("Control de Conteo")]
    [SerializeField] private float lapGracePeriod = 1.0f; // 1 segundo de inmunidad al doble conteo

    // Estado interno
    private int crossingCount = 0; // Cuenta el total de cruces de la meta.
    private bool canCountLap = true; // Permite o bloquea el conteo

    private void Start()
    {
        // Inicializa la interfaz en 0/2
        UpdateLapUI(0);
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        // 1. Verificación básica (Tag y Conteo Activo)
        if (other.CompareTag(playerTag) && canCountLap)
        {
            // Obtener la referencia al motor
            CarroController carController = other.GetComponent<CarroController>();
            if (carController == null) return; // Si no encuentra el script, salimos.

            // 🚨 LÓGICA DE DETECCIÓN DE REVERSA 🚨
            if (carController.IsCarReversing)
            {
                // El contador disminuye al cruzar en reversa, pero nunca por debajo de cero.
                crossingCount = Mathf.Max(0, crossingCount - 1);
                Debug.Log("Cruce en reversa detectado. Contador disminuido.");
            }
            else // Solo si NO está en reversa, contamos el avance.
            {
                crossingCount++;
            }

            // 🚨 DESACTIVA EL CONTEO INMEDIATAMENTE (Anti-Doble Conteo)
            canCountLap = false;

            // 2. Condición de Victoria: Se gana al cruce (N + 1).
            if (crossingCount == targetLaps + 1)
            {
                HandleWinCondition(other.gameObject);
            }
            else
            {
                // Muestra la vuelta actual que se está corriendo
                // El valor a mostrar nunca debe exceder el targetLaps (se queda en 2/2).
                int currentLapToDisplay = Mathf.Min(crossingCount, targetLaps);

                UpdateLapUI(currentLapToDisplay);

                // 3. Reinicia el contador después del periodo de gracia
                StartCoroutine(ResetLapCount());
            }
        }
    }

    private IEnumerator ResetLapCount()
    {
        // Espera el tiempo de gracia (1.0 segundos)
        yield return new WaitForSeconds(lapGracePeriod);

        // Vuelve a habilitar el conteo
        canCountLap = true;
    }

    private void UpdateLapUI(int currentLap)
    {
        // Muestra la vuelta actual que se está corriendo (0/2, 1/2, 2/2)
        lapText.text = $"{currentLap}/{targetLaps} Vueltas";
    }

    private void HandleWinCondition(GameObject player)
    {
        Debug.Log("¡Ganaste!");

        if (lapText != null)
        {
            // Muestra "GANASTE" al final del juego
            lapText.text = "¡GANASTE!";
        }

        CarroController carController = player.GetComponent<CarroController>();

        if (carController != null)
        {
            carController.StopCarOnWin();
        }
    }
}