package fr.pierreyvesmingam.robotr2d2;

/**
 * Created by Pierre-yves on 18/04/2016.
 */
import java.io.ByteArrayOutputStream;
import java.io.Console;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Vector;
import java.util.concurrent.atomic.AtomicBoolean;

import android.os.AsyncTask;
import android.webkit.ConsoleMessage;
import android.widget.TextView;

public class Client extends Thread {

    private String dstAddress;
    private int dstPort;
    private String response = "";
    private TextView textResponse;
    private AtomicBoolean stop;
    private Socket socket;
    private InputStream is;
    private OutputStream os;
    private DataOutputStream dos;
    private Vector<String> outputData;
    private Vector<ClientListener> clientListeners;
    private String envoie;
    private String donneOut;


    Client() {
        this.textResponse=textResponse;
        this.stop = new AtomicBoolean(false);
        this.clientListeners = new Vector<ClientListener>();
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

        this.envoie = message;
    }

    public void run(){
        try{

        System.out.println("ici");
        this.socket = new Socket("192.168.0.3", 12800);
        this.is = socket.getInputStream();
        this.os = socket.getOutputStream();
       // dos = DataOutputStream(OutputStream


        System.out.println("                                                                                                                        LA");
        while(!stop.get()){
            // lecture


            // ecriture
            if(!envoie.isEmpty()) {
                this.dos.writeUTF(envoie);
                outputData.clear();
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
            // if any error occurs
            e.printStackTrace();}
    }

    public interface ClientListener {
        public void onMessageReceived(String message);
    }

}
