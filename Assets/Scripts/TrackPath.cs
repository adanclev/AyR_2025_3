using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(LineRenderer))]
public class TrackPath : MonoBehaviour
{
    public float radioX = 10f; // Ancho del óvalo
    public float radioY = 5f;  // Alto del óvalo
    public int segmentos = 100;
    private LineRenderer lineRenderer;

    void Awake()
    {
        lineRenderer = GetComponent<LineRenderer>();
        lineRenderer.positionCount = segmentos + 1;
        lineRenderer.useWorldSpace = true;
        DrawOval();
    }

    void DrawOval()
    {
        for (int i = 0; i <= segmentos; i++)
        {
            float angulo = (float)i / (float)segmentos * 2 * Mathf.PI;
            float x = Mathf.Sin(angulo) * radioX;
            float y = Mathf.Cos(angulo) * radioY;
            lineRenderer.SetPosition(i, new Vector3(x, y, 0));
        }
    }

    // --- ¡LA FUNCIÓN MÁS IMPORTANTE! ---
    // Encuentra el punto más cercano en el óvalo a una posición dada (la del coche)
    public Vector3 GetClosestPointOnPath(Vector3 carPosition)
    {
        Vector3 closestPoint = Vector3.zero;
        float minDistance = float.MaxValue;

        // Iteramos por todos los segmentos para encontrar el más cercano
        // (Esto se puede optimizar, pero para empezar es perfecto)
        for (int i = 0; i < segmentos; i++)
        {
            Vector3 p1 = lineRenderer.GetPosition(i);
            Vector3 p2 = lineRenderer.GetPosition(i + 1);

            // Función mágica que encuentra el punto más cercano en un segmento de línea
            Vector3 pointOnSegment = ClosestPointOnLineSegment(p1, p2, carPosition);
            float distance = Vector3.Distance(carPosition, pointOnSegment);

            if (distance < minDistance)
            {
                minDistance = distance;
                closestPoint = pointOnSegment;
            }
        }
        return closestPoint;
    }

    // Función auxiliar para GetClosestPointOnPath
    Vector3 ClosestPointOnLineSegment(Vector3 p1, Vector3 p2, Vector3 point)
    {
        Vector3 p1_to_point = point - p1;
        Vector3 p2_to_p1 = p2 - p1;
        float l2 = p2_to_p1.sqrMagnitude;
        if (l2 == 0) return p1;
        float t = Mathf.Clamp01(Vector3.Dot(p1_to_point, p2_to_p1) / l2);
        return p1 + t * p2_to_p1;
    }
}
