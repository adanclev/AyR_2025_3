using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Person : MonoBehaviour
{
    // ¡Esta es la solución a tu duda!
    // La persona se destruye sola después de 5 segundos.
    public float lifeTime = 5f;

    void Start()
    {
        // El coche la verá, frenará, y luego la persona desaparecerá
        // y el coche volverá a acelerar.
        Destroy(gameObject, lifeTime);
    }
}
