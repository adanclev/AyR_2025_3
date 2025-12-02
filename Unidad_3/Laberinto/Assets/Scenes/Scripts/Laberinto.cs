using System.Collections.Generic;
using UnityEngine;

public class GeneradorLaberinto : MonoBehaviour
{
  
    public int filas = 10;
    public int columnas = 10;
    public GameObject paredPrefab; 
    public GameObject pisoPrefab;  
    public Material materialInicio; 
    public Material materialFin;

    private Celda[,] celdas; 
    private Transform laberintoHolder;

    void Start()
    {
        celdas = new Celda[columnas, filas];
        for (int x = 0; x < columnas; x++)
        {
            for (int z = 0; z < filas; z++)
            {
                celdas[x, z] = new Celda();
            }
        }
        GenerarLaberintoLogico();
        ConstruirLaberintoVisual();
    }
    private void OnDrawGizmos()
    {
        if (celdas == null) return;

        for (int x = 0; x < columnas; x++)
        {
            for (int z = 0; z < filas; z++)
            {
               
                Vector3 centro = new Vector3(x, 0, z);
                Celda celda = celdas[x, z];
                if (celda.esPiso)
                {
                    Gizmos.color = Color.green;
                    Gizmos.DrawWireCube(centro, new Vector3(0.5f, 0.1f, 0.5f));
                    if (celda.visitada && !celda.esPiso)
                    {
                        Gizmos.color = Color.yellow;
                        Gizmos.DrawSphere(centro, 0.1f);
                    }
                }
                else
                {
                    Gizmos.color = new Color(0.3f, 0, 0, 0.5f);
                    Gizmos.DrawCube(centro, new Vector3(0.3f, 0.3f, 0.3f));
                }
                Gizmos.color = Color.red;
                if (celda.paredNorte)
                {
                    Vector3 pos = new Vector3(x, 0.5f, z + 0.5f);
                    Gizmos.DrawWireCube(pos, new Vector3(1, 1, 0.1f));
                }
                if (z == 0 && celda.paredSur)
                {
                    Vector3 pos = new Vector3(x, 0.5f, z - 0.5f);
                    Gizmos.DrawWireCube(pos, new Vector3(1, 1, 0.1f));
                }
                if (celda.paredEste)
                {
                    Vector3 pos = new Vector3(x + 0.5f, 0.5f, z);
                    Gizmos.DrawWireCube(pos, new Vector3(0.1f, 1, 1));
                }
                if (x == 0 && celda.paredOeste)
                {
                    Vector3 pos = new Vector3(x - 0.5f, 0.5f, z);
                    Gizmos.DrawWireCube(pos, new Vector3(0.1f, 1, 1));
                }
            }
        }
    }
    void GenerarLaberintoLogico()
    {
        
        Stack<Vector2Int> pila = new Stack<Vector2Int>();
        Vector2Int posActual = new Vector2Int(0, 0);
        celdas[posActual.x, posActual.y].visitada = true;
        pila.Push(posActual);
        while (pila.Count > 0)
        {
           
            posActual = pila.Peek();
            List<Vector2Int> vecinos = ObtenerVecinosNoVisitados(posActual);
            if (vecinos.Count > 0)
            {
              
                Vector2Int vecinoElegido = vecinos[Random.Range(0, vecinos.Count)];

                TumbarPared(posActual, vecinoElegido);
                celdas[vecinoElegido.x, vecinoElegido.y].visitada = true;
                pila.Push(vecinoElegido);
            }
            else
            {
                pila.Pop();
            }
        }
        celdas[columnas - 1, filas - 1].paredEste = false;
    }

    List<Vector2Int> ObtenerVecinosNoVisitados(Vector2Int pos)
    {
        List<Vector2Int> listaVecinos = new List<Vector2Int>();
        int x = pos.x;
        int z = pos.y; 
        if (z + 1 < filas && !celdas[x, z + 1].visitada)
            listaVecinos.Add(new Vector2Int(x, z + 1));
        if (z - 1 >= 0 && !celdas[x, z - 1].visitada)
            listaVecinos.Add(new Vector2Int(x, z - 1)); 
        if (x + 1 < columnas && !celdas[x + 1, z].visitada)
            listaVecinos.Add(new Vector2Int(x + 1, z));

        if (x - 1 >= 0 && !celdas[x - 1, z].visitada)
            listaVecinos.Add(new Vector2Int(x - 1, z));

        return listaVecinos;
    }

    void TumbarPared(Vector2Int actual, Vector2Int vecina)
    {
        celdas[actual.x, actual.y].esPiso = true;
        celdas[vecina.x, vecina.y].esPiso = true;
        if (vecina.x > actual.x)
        {
            celdas[actual.x, actual.y].paredEste = false;
            celdas[vecina.x, vecina.y].paredOeste = false;
        }
        else if (vecina.x < actual.x)
        {
            celdas[actual.x, actual.y].paredOeste = false;
            celdas[vecina.x, vecina.y].paredEste = false;
        }
        else if (vecina.y > actual.y) 
        {
            celdas[actual.x, actual.y].paredNorte = false;
            celdas[vecina.x, vecina.y].paredSur = false;
        }
        else if (vecina.y < actual.y)
        {
            celdas[actual.x, actual.y].paredSur = false;
            celdas[vecina.x, vecina.y].paredNorte = false;
        }
    }
    void ConstruirLaberintoVisual()
    {
        if (laberintoHolder != null) Destroy(laberintoHolder.gameObject);
        laberintoHolder = new GameObject("Laberinto").transform;
        laberintoHolder.parent = this.transform;

        // AJUSTES VISUALES
        float grosorPared = 0.1f; 
        float alturaPared = 1.0f;
        float largoPared = 1.0f;  

        for (int x = 0; x < columnas; x++)
        {
            for (int z = 0; z < filas; z++)
            {
                Celda celda = celdas[x, z];
                if (celda.esPiso)
                {
                    Vector3 posPiso = new Vector3(x, -0.1f, z);
                    GameObject piso = Instantiate(pisoPrefab, posPiso, Quaternion.identity, laberintoHolder);
                    piso.transform.localScale = new Vector3(1, 0.2f, 1);
                    piso.name = $"Piso_{x}_{z}";        
                    MeshRenderer pisoRenderer = piso.GetComponent<MeshRenderer>();

                    if (pisoRenderer != null)
                    {
                        // Inicio
                        if (x == 0 && z == 0)
                        {
                            if (materialInicio != null)
                                pisoRenderer.material = materialInicio;
                            else
                                pisoRenderer.material.color = Color.red;

                            piso.name = "Piso_INICIO";
                        }
                        // Fin 
                        else if (x == columnas - 1 && z == filas - 1)
                        {
                            if (materialFin != null)
                                pisoRenderer.material = materialFin;
                            else
                                pisoRenderer.material.color = Color.green;
                            piso.name = "Piso_FIN";
                            piso.tag = "Meta";
                            BoxCollider trigger = piso.AddComponent<BoxCollider>();                     
                            trigger.isTrigger = true;                     
                            trigger.size = new Vector3(1, 10, 1);                  
                            trigger.center = new Vector3(0, 5, 0);
                        }
                    }
                }
                // Pared Norte (Arriba)
                if (celda.paredNorte)
                {
                    Vector3 pos = new Vector3(x, 0.5f, z + 0.5f);
                    GameObject pared = Instantiate(paredPrefab, pos, Quaternion.identity, laberintoHolder);
                    // ESCALA: Ancho X=1, Alto Y=1, Grosor Z=0.1
                    pared.transform.localScale = new Vector3(largoPared, alturaPared, grosorPared);
                    pared.name = $"ParedNorte_{x}_{z}";
                }
                // Pared Sur 
                if (z == 0 && celda.paredSur)
                {
                    Vector3 pos = new Vector3(x, 0.5f, z - 0.5f);
                    GameObject pared = Instantiate(paredPrefab, pos, Quaternion.identity, laberintoHolder);
                    pared.transform.localScale = new Vector3(largoPared, alturaPared, grosorPared);
                    pared.name = $"ParedSur_{x}_{z}";
                }
                // Pared Este 
                if (celda.paredEste)
                {
                    Vector3 pos = new Vector3(x + 0.5f, 0.5f, z);
                    GameObject pared = Instantiate(paredPrefab, pos, Quaternion.identity, laberintoHolder);
                    
                    pared.transform.localScale = new Vector3(grosorPared, alturaPared, largoPared);
                    pared.name = $"ParedEste_{x}_{z}";
                }
                // Pared Oeste
                if (x == 0 && celda.paredOeste)
                {
                    Vector3 pos = new Vector3(x - 0.5f, 0.5f, z);
                    GameObject pared = Instantiate(paredPrefab, pos, Quaternion.identity, laberintoHolder);
                    pared.transform.localScale = new Vector3(grosorPared, alturaPared, largoPared);
                    pared.name = $"ParedOeste_{x}_{z}";
                }
            }
        }
    }
}

[System.Serializable]
public class Celda
{
    public bool visitada = false;
    public bool paredNorte = true;
    public bool paredSur = true;
    public bool paredEste = true;
    public bool paredOeste = true;
    public bool esPiso = false;
}