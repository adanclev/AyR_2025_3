using TMPro;
using UnityEngine;

public class SpeedometerUI : MonoBehaviour
{
    [SerializeField] Rigidbody2D carRb2D;
    [SerializeField] TextMeshProUGUI speedText;

    void Update()
    {
        float speed = carRb2D.linearVelocity.magnitude * 3.6f;
        speedText.text = Mathf.RoundToInt(speed).ToString();
    }
}
