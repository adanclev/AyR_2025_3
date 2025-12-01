using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public GameObject personPrefab; 
    public TrackPath track;

    // Esta función la conectarás al OnClick() del botón en el Inspector
    public void SpawnPerson()
    {
        // Elige un punto aleatorio en el óvalo para aparecer
        int randomSegment = Random.Range(0, track.segmentos);
        Vector3 spawnPoint = track.GetComponent<LineRenderer>().GetPosition(randomSegment);

        Instantiate(personPrefab, spawnPoint, Quaternion.identity);
    }
}
