package fr.pierreyvesmingam.robotr2d2;

import org.json.JSONObject;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Created by Pierre-yves on 12/05/2016.
 */
public class Serveur extends Thread{

    private Socket socket2;
    private String envoiVideo;
    private ServerListener serveurListener;
    String line;


    Serveur() throws IOException
    {


    }



    public void startServeur() throws IOException {
        //initialise ton socket
        this.start();
    }

    public void addServeurListener(ServerListener serveurListener) {
        this.serveurListener = serveurListener;
    }

    public interface ServerListener {
        public void onVideoRecieved(String message);
    }

    public void stopServeur() {
        try {
            socket2.close();
            this.serveurListener.onVideoRecieved("Serveur déconnecté...");
        } catch (IOException e1) {
            e1.printStackTrace();

        }
    }



    /**
     * Thread event loop | this part wait for handle an event and apply a spcific function bind by on method
     */
    /*public void run() {
        try {
            while(( socket = serverSocket.accept()) != null )
            {
                BufferedReader in;
                in = new BufferedReader(new InputStreamReader(this.socket.getInputStream()));
                line = null;
                System.out.println("dans le thread reception");
                while ((line = in.readLine()) != null) {
                    if (serveurListener == null) System.out.println("null clientListener");
                    else
                        serveurListener.onVideoRecieved(line);
                    System.out.println(line);
                    System.out.println("doit recevoir dans la CLASS SERVEURURURURURURRURURURU");
                }
                System.out.println("Je suis sorti de ma boucle MGL");
            }
        }catch (IOException e1) {
            e1.printStackTrace();
            System.out.println("La reception à été coupé");
        }
    }*/
    public void run() {

        this.socket2         = null;
        BufferedReader in;
        DataOutputStream out  = null;
        JSONObject jsonObject = null;
        JSONObject data       = null;
        ServerSocket serverSocket = null;
        try {
            serverSocket = new ServerSocket( 12801 );
            System.out.println("Je suis dans le run du serveur");
            while(( this.socket2 = serverSocket.accept()) != null ) {
                System.out.println("                                           J AI RECU DES TRUCS OUAISSS ENFIN.............................");
                in = new  BufferedReader(new InputStreamReader(this.socket2.getInputStream()));
                line = null;
                System.out.println("dans le thread reception");
                while ((line = in.readLine()) != null) {
                    if (serveurListener == null) System.out.println("null clientListener");
                    else
                    serveurListener.onVideoRecieved(line);
                    System.out.println(line);
                    System.out.println("doit recevoir dans la CLASS SERVEURURURURURURRURURURU");
                }
                System.out.println("Je suis sorti de ma boucle MGL");
            }


            } catch (IOException e1) {
            e1.printStackTrace();
        }
    }
}
