package fr.pierreyvesmingam.robotr2d2.helper;

import android.content.Context;
import android.os.SystemClock;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Calendar;

import fr.pierreyvesmingam.robotr2d2.Client;

/**
 * Created by steven_watremez on 08/06/16.
 */
public class RobotMoveHelper {
    /*
    * ************************************************************************
    * PUBLIC STATIC METHODS
    * ************************************************************************
    */

    /**
     * mode 8 to stop robot's motors
     */
    public static void stopMotors(@Nullable final Client client) {
        // Perform action on click
        final JSONObject deconnectionJSON = new JSONObject();
        try {
            final String leftSpeed = "0000";
            final String rightSpeed = "0000";
            final Calendar cal = Calendar.getInstance();
            final String millisecondToString = String.valueOf(cal.getTimeInMillis());

            deconnectionJSON.put("mode", "8"); //mode 8 to stop robot activity
            deconnectionJSON.put("vitesseG", rightSpeed); //vitesse moteur de gauche
            deconnectionJSON.put("vitesseD", leftSpeed); //vitesse moteur de gauche
            deconnectionJSON.put("temps", millisecondToString); //vitesse moteur de gauche
        } catch (JSONException e) {
            e.printStackTrace();
        }

        final String deconnectionJsonToString = deconnectionJSON.toString(); // convertie le JSON en string pour l'envoyer
        if (client != null) {
            client.sendMessage(deconnectionJsonToString);
        }
    }

    /**
     * mode 0 to move the robot with left and right speed for wheels
     */
    public static void launchMotorsWithModeZero(@Nullable final Client client, @NonNull final String rightSpeed, @NonNull final String leftSpeed) {

        final JSONObject emissionJSON = new JSONObject();
        try {
            final Calendar cal = Calendar.getInstance();
            final String millisecondToString = String.valueOf(cal.getTimeInMillis());
            emissionJSON.put("mode", "0"); //mode 0 pour landscape
            emissionJSON.put("vitesseG", leftSpeed); //vitesse moteur de gauche
            emissionJSON.put("vitesseD", rightSpeed); //vitesse moteur de gauche
            emissionJSON.put("temps", millisecondToString);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        final String emissionJSONToString = emissionJSON.toString(); // convertie le JSON en string pour l'envoyer
        if (client != null) {
            client.sendMessage(emissionJSONToString);
        }
    }

    /**
     * mode 2 to move the robot with just angle and speed value
     */
    public static void launchMotorsWithModeTwo(@Nullable final Client client, @NonNull final String angle, @NonNull final String speed) {
        //mode 2 to use angle with the robot
        final JSONObject emissionJSON = new JSONObject();
        try {
            final Calendar cal = Calendar.getInstance();
            final String millisecondToString = String.valueOf(cal.getTimeInMillis());
            emissionJSON.put("mode", "2");
            emissionJSON.put("angle", angle);
            emissionJSON.put("vitesse", speed);
            emissionJSON.put("temps", millisecondToString);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        final String emissionJSONToString = emissionJSON.toString(); // convertie le JSON en string pour l'envoyer
        if (client != null) {
            client.sendMessage(emissionJSONToString);
        }
    }

    public static String motorSpeedCalcul(int speed) {
        boolean megaG = false;

        //speed = Math.round(speed / 100 * 127);
        String speedString = Integer.toString(speed);
        if (speed < 0) {
            megaG = true;
        } else if (speed == 0) {
            speedString = "0000";
        }

        switch (speedString.length()) {
            case 1:
                speedString = megaG ? speedString : "000" + speedString;
                break;
            case 2:
                speedString = megaG ? "-00" + Integer.toString(Math.abs(Math.round(speed))) : "00" + speedString;
                break;
            case 3:
                speedString = megaG ? "-0" + Integer.toString(Math.abs(Math.round(speed))) : "0" + speedString;
                break;
        }
        return speedString;
    }

    /**
     * start the connexion to the robot
     */
    public static Client robotConnection(@Nullable Client client, @NonNull final Client.ClientListener listener) {
        if (client == null) {
            client = new Client();
            client.addClientListener(listener);
        }
        client.startClient();
        return client;
    }

    /**
     * stop the connexion to the robot
     */
    public static void robotDeconnection(@NonNull final Client client, @NonNull final Context context) {

        final JSONObject deconnectionJSON = new JSONObject();
        try {
            deconnectionJSON.put("connexion", "false");
        } catch (JSONException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        final String deconnectionJSONtoString = deconnectionJSON.toString(); // converti le JSON en string pour l'envoyer
        client.sendMessage(deconnectionJSONtoString);
        SystemClock.sleep(100);
        client.stopClient();
    }


}
