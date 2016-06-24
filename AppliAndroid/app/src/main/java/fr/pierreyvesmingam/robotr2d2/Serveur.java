package fr.pierreyvesmingam.robotr2d2;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * Created by Pierre-yves on 12/05/2016.
 */
public class Serveur extends Thread {

    String line;
    private Socket socket2;
    private String envoiVideo;
    private ServerListener serveurListener;

    Serveur() {
    }

    public void startServeur() {
        //initialise ton socket
        this.start();
    }

    public void addServeurListener(ServerListener serveurListener) {
        this.serveurListener = serveurListener;
    }

    public void stopServeur() {
        try {
            socket2.close();
            this.serveurListener.onVideoRecieved("Serveur déconnecté...");
        } catch (IOException e1) {
            e1.printStackTrace();

        }
    }

    public void run() {

        this.socket2 = null;
        BufferedReader in;
        DataOutputStream out = null;
        JSONObject jsonObject = null;
        JSONObject data = null;
        ServerSocket serverSocket = null;
        try {
            serverSocket = new ServerSocket(12801);
            System.out.println("Je suis dans le run du serveur");
            while ((this.socket2 = serverSocket.accept()) != null) {
                in = new BufferedReader(new InputStreamReader(this.socket2.getInputStream()));
                line = null;
                System.out.println("dans le thread reception");
                while ((line = in.readLine()) != null) {
                    if (serveurListener == null) System.out.println("null clientListener");
                    else
                        serveurListener.onVideoRecieved(line);
                    System.out.println(line);
                }
            }

        } catch (IOException e1) {
            e1.printStackTrace();
        }
    }

    public interface ServerListener {
        public void onVideoRecieved(String message);
    }
}
