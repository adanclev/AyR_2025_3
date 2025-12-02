using UnityEngine;
using System.Collections;

public class SolverManoDerecha : MonoBehaviour
{
    public float tiempoEspera = 0.5f; 
    public bool haTerminado = false;

    void Start()
    {
        StartCoroutine(ResolverLaberinto());
    }

    IEnumerator ResolverLaberinto()
    {
        yield return new WaitForSeconds(1f);

        while (!haTerminado)
        {
            if (!HayPared(Vector3.right))
            {
                yield return Girar(90);
                yield return Moverse();
            }
            else if (!HayPared(Vector3.forward))
            {
                yield return Moverse();
            }
            else
            {
                yield return Girar(-90);
            }
            yield return new WaitForSeconds(tiempoEspera);
        }
    }
    bool HayPared(Vector3 direccionLocal)
    {
        Vector3 direccionMundo = transform.TransformDirection(direccionLocal);
        if (Physics.Raycast(transform.position, direccionMundo, out RaycastHit hit, 0.8f))
        {
            if (hit.collider.isTrigger) return false;

            return true; 
        }
        return false; 
    }
    IEnumerator Moverse()
    {
        Vector3 posicionInicial = transform.position;
        Vector3 destino = transform.position + transform.forward;
        float tiempoPasado = 0;
        float duracion = 0.3f; 
        while (tiempoPasado < duracion)
        {
            transform.position = Vector3.Lerp(posicionInicial, destino, tiempoPasado / duracion);
            tiempoPasado += Time.deltaTime;
            yield return null;
        }
        transform.position = destino;
    }
    IEnumerator Girar(float angulo)
    {
        Quaternion rotacionInicial = transform.rotation;
        Quaternion rotacionFinal = rotacionInicial * Quaternion.Euler(0, angulo, 0);

        float tiempoPasado = 0;
        float duracion = 0.3f;

        while (tiempoPasado < duracion)
        {
            transform.rotation = Quaternion.Lerp(rotacionInicial, rotacionFinal, tiempoPasado / duracion);
            tiempoPasado += Time.deltaTime;
            yield return null;
        }
        transform.rotation = rotacionFinal;
    }
    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Meta"))
        {
            Debug.Log("¡EL BOT HA GANADO!");
            haTerminado = true;
            StopAllCoroutines(); // Detener el cerebro
        }
    }
}