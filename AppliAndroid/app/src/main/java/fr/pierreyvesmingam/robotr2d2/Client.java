package fr.pierreyvesmingam.robotr2d2;

/**
 * Created by Pierre-yves on 18/04/2016.
 */
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.ConnectException;
import java.net.Socket;
import java.sql.Connection;
import java.util.Calendar;
import java.util.Vector;
import java.util.concurrent.atomic.AtomicBoolean;

import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

public class Client extends Thread {

    private String dstAddress,line;
    private int dstPort;
    private String response = "";
    private TextView textResponse;
    private AtomicBoolean stop;
    private Boolean connected;
    private Socket socket;
    private InputStream is;
    private OutputStream os;
    private DataOutputStream dos;
    private DataInputStream dis;
    private Vector<String> outputData;
    private ClientListener clientListener;
    private String envoieMessage;
    private String donneOut;
    private JSONObject JSONNul;
    private String stringNulQuandPasEnvoi = new String();
    private String millisToString;
    private int enculeDeConnexion;
    private InputStreamReader isr;
    private BufferedReader br;
    private Reception r;
    private Emission e;

    Client() {
        this.textResponse=textResponse;
        this.stop = new AtomicBoolean(false);
        this.connected = false;
        this.envoieMessage = new String();
        this.JSONNul = new JSONObject();
        this.enculeDeConnexion = 0;
        e = new Emission();
        r = new Reception();

    }
        /*Methode startClient */
    //
    // Permet le lancement du thread Client qui lui lance la connexion et le thread emission et reception
    //
    //
        public void startClient() throws IOException {
            //initialise ton socket
            this.start();
        }
        public void run()
        {
            System.out.println("ici");
            try {
                socket = new Socket("172.16.0.2", 12800);
                System.out.println("La connexion a été faite");
                e.setSocket(socket);
                r.setSocket(socket);
                r.start();
                e.start();
                System.out.println("Les threads on été correctement lancés");
            } catch (IOException e1) {
                e1.printStackTrace();
            }


        }

        public void stopClient() {
            stop.set(false);
        }

        public void addClientListener(ClientListener clientListener) {
            this.clientListener = clientListener;
        }

        /*Methode sendMessage */
        //
        // Permet de recuperer le message envoyé de l'activity et de l'envoyer dans le thread emission
        //
        //
        public void sendMessage(String message) {

            this.envoieMessage = message;
            System.out.println("initialisation message envoie");
            System.out.println(this.envoieMessage);
        }

        public int getConnxion()
        {
            return enculeDeConnexion = 0;
        }

    public interface ClientListener {
        public void onMessageReceived(String message);
    }

    /******************************************/
    /*           Class de Reception          */
    /****************************************/
    private class Reception extends Thread
    {

        private Socket socket;

        public void setSocket(Socket socket) {
            this.socket = socket;
        }

        public void run()
        {
            //lecture
           try {
            BufferedReader in ;
            in = new BufferedReader(new InputStreamReader(this.socket.getInputStream()));
            line = null;
            System.out.println("dans le thread reception");
            while ((line = in.readLine()) != null) {
                System.out.println(line);
                System.out.println("doit recevoir");
            }
            System.out.println("Je suis sorti de ma boucle MGL");
            }catch (IOException e1) {
            e1.printStackTrace();
            System.out.println("La reception à été coupé");
            }

            /*
            java.util.Scanner s = new java.util.Scanner(is).useDelimiter("\\A");
            if(s.hasNext())
            {
                String message = s.next(); // je prend le qlq chose pour le mettre dans le message
                clientListener.onMessageReceived(message);
                System.out.println(message);

            }*/
        }
    }

    /******************************************/
    /*           Class de Emission           */
    /****************************************/
    private class Emission extends Thread {
        private Socket socket;

        public void setSocket(Socket socket) throws IOException {
            this.socket = socket;
            os = socket.getOutputStream();
            dos = new DataOutputStream(os);
        }

        public void run() {

            try {
                while (!stop.get()) {
                    // ecriture
                    if (!envoieMessage.isEmpty()) {
                        System.out.println("Je suis dans une magnifique boucle");
                        dos.writeUTF(envoieMessage);
                        envoieMessage = "";

                    } else if (envoieMessage.isEmpty()) {
                        Calendar cal = Calendar.getInstance();
                        millisToString = new String(String.valueOf(cal.getTimeInMillis()));
                        System.out.println("Inactivité !");

                        JSONNul.put("mode", "8"); //mode 0 pour landscape

                        JSONNul.put("vitesseG", "0000"); //vitesse moteur de gauche
                        JSONNul.put("vitesseD", "0000"); //vitesse moteur de gauche
                        JSONNul.put("temps", millisToString); //vitesse moteur de gauche
                        System.out.println(JSONNul.toString());
                        stringNulQuandPasEnvoi = JSONNul.toString();
                        dos.writeUTF(stringNulQuandPasEnvoi);
                        stringNulQuandPasEnvoi = "";

                    }
                    this.sleep(80);
                }
            } catch (ConnectException ex) {
                enculeDeConnexion = 0;
            } catch (Exception e) {

                System.out.println("L'emission à été coupé");
                e.printStackTrace();
            }

        }
    }
}



//  public void run() {
           /* try {
                System.out.println("ici");
                this.socket = new Socket("172.16.0.2", 12800);
                System.out.println("LAAAAAA");
                this.enculeDeConnexion = 1;
                this.is = socket.getInputStream();
                this.os = socket.getOutputStream();
                dos = new DataOutputStream(os);
                dis = new DataInputStream(this.is);
                // dos = DataOutputStream(OutputStream
                connected = true;*/
       /* while(!stop.get()){
            // ecriture
            if(!this.envoieMessage.isEmpty()) {
                System.out.println("Je suis dans une magnifique boucle");
                System.out.println("LE MESSAGE A L4ENVOI EST EXACTEMENT CELUI LA LALALALALLALALALALALALA : "+ this.envoieMessage);
                this.dos.writeUTF(this.envoieMessage);
                envoieMessage="";

            }
            else if (this.envoieMessage.isEmpty())
            {
                Calendar cal = Calendar.getInstance();
                millisToString = new String(String.valueOf(cal.getTimeInMillis()));
                System.out.println("Inactivité !");
                JSONNul.put("mode", "8"); //mode 0 pour landscape
                JSONNul.put("vitesseG", "0000"); //vitesse moteur de gauche
                JSONNul.put("vitesseD", "0000"); //vitesse moteur de gauche
                JSONNul.put("temps", millisToString); //vitesse moteur de gauche
                System.out.println(JSONNul.toString());
                stringNulQuandPasEnvoi = JSONNul.toString();
                this.dos.writeUTF(this.stringNulQuandPasEnvoi);
                stringNulQuandPasEnvoi="";

            }

            //lecture

            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            line = null;
            while ((line = in.readLine()) != null) {
                System.out.println(line);
                System.out.println("doit recevoir");
            }
            System.out.println("Je suis sorti de ma boucle MGL");

            java.util.Scanner s = new java.util.Scanner(is).useDelimiter("\\A");
            if(s.hasNext())
            {
                String message = s.next(); // je prend le qlq chose pour le mettre dans le message
                    this.clientListener.onMessageReceived(message);
                    System.out.println(message);

            }

            this.sleep(80);
        }
        }catch (ConnectException ex){
            enculeDeConnexion = 0;
        }
        catch(Exception e){

            System.out.println("JE SUIS DANS LE CATCH DU CLIENT!");
            e.printStackTrace();
        }
            }
        }
    }*/