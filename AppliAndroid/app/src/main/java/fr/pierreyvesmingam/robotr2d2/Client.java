package fr.pierreyvesmingam.robotr2d2;

/**
 * Created by Pierre-yves on 18/04/2016.
 */
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.util.Vector;
import java.util.concurrent.atomic.AtomicBoolean;

import android.widget.TextView;

public class Client extends Thread {

    private String dstAddress;
    private int dstPort;
    private String response = "";
    private TextView textResponse;
    private AtomicBoolean stop;
    private Boolean connected;
    private Socket socket;
    private InputStream is;
    private OutputStream os;
    private DataOutputStream dos;
    private Vector<String> outputData;
    private Vector<ClientListener> clientListeners;
    private String envoieMessage;
    private String donneOut;


    Client() {
        this.textResponse=textResponse;
        this.stop = new AtomicBoolean(false);
        this.connected = false;
        this.clientListeners = new Vector<ClientListener>();
        this.envoieMessage = new String();
    }

    public void initClient() throws IOException {
    }

    public void startClient(){
        this.start();
    }

    public void stopClient(){
        stop.set(false);
    }

    public void addClientListener(ClientListener clientListener){
        this.clientListeners.add(clientListener);
    }

    public void sendMessage(String message){

        this.envoieMessage = message;
        System.out.println("initialisation message envoie");
        System.out.println(this.envoieMessage);
    }

    public void run(){
        try{

        System.out.println("ici");
        this.socket = new Socket("192.168.0.2", 12800);
        connected = true;
        this.is = socket.getInputStream();
        this.os = socket.getOutputStream();
        dos = new DataOutputStream(os);
       // dos = DataOutputStream(OutputStream
        connected= true;
        while(!stop.get()){
            // lecture


            // ecriture
            if(!this.envoieMessage.isEmpty()) {
                System.out.println("Je suis dans une magnifique boucle");
                this.dos.writeUTF(this.envoieMessage);
                outputData.clear();
                this.sleep(80);
            }

            for(ClientListener clientListener : clientListeners)
                clientListener.onMessageReceived("coucou");
                try {
                this.sleep(80);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
        }
        }catch(Exception e){
            connected = false;
            e.printStackTrace();
        }
    }

    public interface ClientListener {
        public void onMessageReceived(String message);
    }

    public Boolean getConnected() {
        return connected;
    }


}
