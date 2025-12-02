using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Jugador : MonoBehaviour
{
    public float velocidadMovimiento = 3.0f;
    public float velocidadRotacion = 150.0f;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {  
        float moverZ = Input.GetAxis("Vertical") * velocidadMovimiento * Time.deltaTime;
        float rotarY = Input.GetAxis("Horizontal") * velocidadRotacion * Time.deltaTime;
        transform.Translate(0, 0, moverZ);
        transform.Rotate(0, rotarY, 0);
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Meta"))
        {
            Debug.Log("¡GANASTE! Juego Pausado.");
            Time.timeScale = 0;
        }
    }
}