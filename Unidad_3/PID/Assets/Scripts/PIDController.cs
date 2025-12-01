using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable] // Para que puedas ver y editar Kp, Ki, Kd en el Inspector de Unity
public class PIDController
{
    public float Kp = 1f; // Proporcional
    public float Ki = 0f; // Integral
    public float Kd = 0.1f; // Derivativo

    private float integral;
    private float lastError;

    public float Calculate(float setpoint, float measurement)
    {
        // 1. Calcular el Error
        float error = setpoint - measurement;

        // 2. Calcular la parte Proporcional
        float proportional = Kp * error;

        // 3. Calcular la parte Integral
        integral += error * Time.fixedDeltaTime;
        float integralTerm = Ki * integral;

        // 4. Calcular la parte Derivativa
        float derivative = (error - lastError) / Time.fixedDeltaTime;
        float derivativeTerm = Kd * derivative;

        lastError = error;

        // 5. Sumar todo y retornar la salida
        return proportional + integralTerm + derivativeTerm;
    }

    public void Reset()
    {
        integral = 0;
        lastError = 0;
    }
}
