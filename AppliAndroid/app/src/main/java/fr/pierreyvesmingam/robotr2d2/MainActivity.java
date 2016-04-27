package fr.pierreyvesmingam.robotr2d2;

import android.content.Intent;
import android.os.Bundle;
import android.app.Activity;
import android.support.v7.app.AppCompatActivity;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.OnTouchListener;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;
import java.net.UnknownHostException;
import android.os.AsyncTask;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity implements Client.ClientListener {

    RelativeLayout layout_joystick, layout_joystick2,layout_joystick3;
    ImageView image_joystick, image_border;
    TextView textView3, textView4, textView5,vitesse, etatBatterie, probleme, textView2,textView18;

    JoyStickClass js,js2,js3;

    String vitesseG,vitesseD,valAccel,anglePortrait,vitessePortrait;
    float intVitesseG,intVitesseD;

    JSONObject donneEnvoiJSON = new JSONObject();
    JSONObject donneEnvoiJSONPortrait = new JSONObject();
    private  Client socketLandscape;
    private  Client socketPortrait;
    private boolean AppuiConnexionPaysage = false;
    private boolean AppuiConnexionPortrait = false;
    private boolean ListenerOrNot1 = false;

    public static boolean IS_LANDSCAPE = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Client client = new Client();
        client.addClientListener(this);
        textView3 = (TextView) findViewById(R.id.textView3);
        textView4 = (TextView) findViewById(R.id.textView4);
        textView5 = (TextView) findViewById(R.id.textView5);
        textView2 = (TextView) findViewById(R.id.textView2);
        textView18 = (TextView) findViewById(R.id.textView18);
        probleme = (TextView) findViewById(R.id.probleme);

        layout_joystick = (RelativeLayout) findViewById(R.id.layout_joystick);
        layout_joystick2 = (RelativeLayout) findViewById(R.id.layout_joystick2);
        layout_joystick3 = (RelativeLayout) findViewById(R.id.layout_joystick3);


        valAccel = new String();

        boolean mega = false;


        MainActivity.IS_LANDSCAPE = getResources().getBoolean(R.bool.isLandscape);

            if(MainActivity.IS_LANDSCAPE) {
                                                                                    //paysage
                socketLandscape = new Client(); //creation socket
                final Button button = (Button) findViewById(R.id.button8);
                button.setOnClickListener(new View.OnClickListener() {
                    public void onClick(View v) {
                        // Perform action on click
                        System.out.println("Je suis dans le bouton connexion");
                        AppuiConnexionPaysage = true;
                        socketLandscape.startClient();
                        if (socketLandscape.getConnected()) {
                            Toast.makeText(getApplicationContext(), "Connected", Toast.LENGTH_SHORT).show();
                        } else {
                            Toast.makeText(getApplicationContext(), "Connection refused", Toast.LENGTH_SHORT).show();
                        }
                    }
                });

                //joystick 1, a gauche sur vu paysage
                js3 = new JoyStickClass(getApplicationContext(), layout_joystick3, R.drawable.rouge);
                js3.setStickSize(150, 150);
                js3.setLayoutSize(500, 500);
                js3.setLayoutAlpha(150);
                js3.setStickAlpha(100);
                js3.setOffset(90);
                js3.setMinimumDistance(50);


                layout_joystick3.setOnTouchListener(new OnTouchListener() {
                    public boolean onTouch(View arg0, MotionEvent arg1) {
                        js3.drawStick(arg1);
                        ListenerOrNot1 = true;
                        if (arg1.getAction() == MotionEvent.ACTION_DOWN
                                || arg1.getAction() == MotionEvent.ACTION_MOVE) {
                            intVitesseG = new Float(Math.round(js3.getDistance()));
                            vitesseG = new String(String.valueOf(Math.round(js3.getDistance())));
                            textView4.setText("Vitesse G : " + vitesseG);

                            //mise en forme pour le JSON des vitesse
                            int direction = js3.get8Direction();
                            if (direction == JoyStickClass.STICK_UP) {
                                textView5.setText("Direction G : Up");
                            } else if (direction == JoyStickClass.STICK_UPRIGHT) {
                                textView5.setText("Direction G: Up");
                            } else if (direction == JoyStickClass.STICK_RIGHT) {
                                textView5.setText("Direction G: Center");
                            } else if (direction == JoyStickClass.STICK_DOWNRIGHT) {
                                textView5.setText("Direction G: Down");
                            } else if (direction == JoyStickClass.STICK_DOWN) {
                                textView5.setText("Direction G: Down");
                            } else if (direction == JoyStickClass.STICK_DOWNLEFT) {
                                textView5.setText("Direction G: Down");
                            } else if (direction == JoyStickClass.STICK_LEFT) {
                                textView5.setText("Direction G: Center");
                            } else if (direction == JoyStickClass.STICK_UPLEFT) {
                                textView5.setText("Direction G: Up");
                            } else if (direction == JoyStickClass.STICK_NONE) {
                                textView5.setText("Direction G: Center");
                            }
                        } else if (arg1.getAction() == MotionEvent.ACTION_UP) {


                            textView4.setText("Distance G:");
                            textView5.setText("Direction G:");
                        }
                        vitesseG = Integer.toString((Math.round(intVitesseG/100*127)));
                        intVitesseG = Math.round(intVitesseD/100*127);
                        boolean megaG = false;
                        if (intVitesseG < 0) {
                            megaG = true;
                        }
                        else if(intVitesseG == 0)
                        {
                            vitesseG = "0000";
                        }
                        if (megaG) {
                            if (vitesseG.length() == 2) {

                                vitesseG = "-00" + Integer.toString(Math.abs(Math.round(intVitesseG)));
                                System.out.println(vitesseG);
                            }
                            if (vitesseG.length() == 3) {
                                vitesseG = "-0" + Integer.toString(Math.abs(Math.round(intVitesseG)));
                            }
                        } else {
                            if (vitesseG.length() == 1) {
                                vitesseG = "000" + vitesseG;
                            } else if (vitesseG.length() == 2) {
                                vitesseG = "00" + vitesseG;
                            } else if (vitesseG.length() == 3) {
                                vitesseG = "0" + vitesseG;
                            }
                        }
                        return true;
                    }

                });


                //joystick 2, a droite sur vu paysage
                js2 = new JoyStickClass(getApplicationContext(), layout_joystick2, R.drawable.rouge);
                js2.setStickSize(150, 150);
                js2.setLayoutSize(500, 500);
                js2.setLayoutAlpha(150);
                js2.setStickAlpha(100);
                js2.setOffset(90);
                js2.setMinimumDistance(50);

                layout_joystick2.setOnTouchListener(new OnTouchListener() {
                    public boolean onTouch(View arg0, MotionEvent arg1) {
                        AppuiConnexionPaysage = true;
                        js2.drawStick(arg1);
                        if (arg1.getAction() == MotionEvent.ACTION_DOWN
                                || arg1.getAction() == MotionEvent.ACTION_MOVE) {

                            intVitesseD = new Float(Math.round(js2.getDistance()));
                            vitesseD = new String(String.valueOf(intVitesseD));

                            textView2.setText("Vitesse D: " + vitesseD);

                            int direction = js2.get8Direction();
                            if (direction == JoyStickClass.STICK_UP) {
                                textView18.setText("Direction D: Up");
                            } else if (direction == JoyStickClass.STICK_UPRIGHT) {
                                textView18.setText("Direction D: Up");
                            } else if (direction == JoyStickClass.STICK_RIGHT) {
                                textView18.setText("Direction D: Center");
                            } else if (direction == JoyStickClass.STICK_DOWNRIGHT) {
                                textView18.setText("Direction D: Down");
                            } else if (direction == JoyStickClass.STICK_DOWN) {
                                textView18.setText("Direction D: Down");
                            } else if (direction == JoyStickClass.STICK_DOWNLEFT) {
                                textView18.setText("Direction D: Down");
                            } else if (direction == JoyStickClass.STICK_LEFT) {
                                textView18.setText("Direction D: Center");
                            } else if (direction == JoyStickClass.STICK_UPLEFT) {
                                textView18.setText("Direction D: Up");
                            } else if (direction == JoyStickClass.STICK_NONE) {
                                textView18.setText("Direction D: Center");
                            }
                        } else if (arg1.getAction() == MotionEvent.ACTION_UP) {


                            textView2.setText("Distance D:");
                            textView18.setText("Direction D:");
                        }
                        boolean megaG = false;
                        vitesseD = Integer.toString((Math.round(intVitesseD / 100 * 127)));
                        intVitesseD = Math.round(intVitesseD / 100 * 127);
                        if (intVitesseD < 0) {
                            megaG = true;
                        } else if (intVitesseD == 0) {
                            vitesseD = "0000";
                        }
                        if (megaG) {

                            if (vitesseD.length() == 2) {
                                vitesseD = "-00" + Integer.toString(Math.abs(Math.round(intVitesseD)));
                            }
                            if (vitesseD.length() == 3) {
                                vitesseD = "-0" + Integer.toString(Math.abs(Math.round(intVitesseD)));
                                System.out.println("Are You Here My Brother Friend ?");
                            }
                        } else {
                            if (vitesseD.length() == 1) {
                                vitesseD = "000" + vitesseD;
                            } else if (vitesseD.length() == 2) {
                                vitesseD = "00" + vitesseD;
                            } else if (vitesseD.length() == 3) {
                                vitesseD = "0" + vitesseD;
                            }
                        }


                        try {
                            donneEnvoiJSON.put("mode", "0"); //mode 0 pour landscape
                            donneEnvoiJSON.put("vitesseG", vitesseG); //vitesse moteur de gauche
                            donneEnvoiJSON.put("vitesseD", vitesseD); //vitesse moteur de gauche
                        } catch (JSONException e) {
                            // TODO Auto-generated catch block
                            e.printStackTrace();
                        }

                        String donneJsonToString = donneEnvoiJSON.toString(); // convertie le JSON en string pour l'envoyer
                        socketLandscape.sendMessage(donneJsonToString);
                        return true;
                    }
                });

                probleme.setText("Problème: " + socketLandscape);
            }
            else {
                                                 //portrait
            socketPortrait = new Client(); //creation socket
            final Button button = (Button) findViewById(R.id.button7);
            button.setOnClickListener(new View.OnClickListener() {
                public void onClick(View v) {
                    // Perform action on click
                    AppuiConnexionPortrait = true;
                    socketPortrait.startClient();
                    if (socketPortrait.getConnected()) {
                        Toast.makeText(getApplicationContext(), "Connected", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(getApplicationContext(), "Connection refused", Toast.LENGTH_SHORT).show();
                    }
                }
            });


                //connexion(socketPortrait);
                //joystick principale en mode portrait
                js = new JoyStickClass(getApplicationContext(), layout_joystick, R.drawable.rouge);
                js.setStickSize(150, 150);
                js.setLayoutSize(500, 500);
                js.setLayoutAlpha(150);
                js.setStickAlpha(100);
                js.setOffset(90);
                js.setMinimumDistance(50);

            layout_joystick.setOnTouchListener(new OnTouchListener() {
                public boolean onTouch(View arg0, MotionEvent arg1) {
                    AppuiConnexionPortrait = true;
                    js.drawStick(arg1);
                    if (arg1.getAction() == MotionEvent.ACTION_DOWN
                            || arg1.getAction() == MotionEvent.ACTION_MOVE) {

                        anglePortrait = new String(String.valueOf(Math.round(js.getAngle())));
                        vitessePortrait = new String(String.valueOf(Math.round(js.getDistance())));

                        textView3.setText("Angle : " + anglePortrait);
                        textView4.setText("Distance : " + vitessePortrait);

                        int direction = js.get8Direction();
                        if (direction == JoyStickClass.STICK_UP) {
                            textView5.setText("Direction : Up");
                        } else if (direction == JoyStickClass.STICK_UPRIGHT) {
                            textView5.setText("Direction : Up Right");
                        } else if (direction == JoyStickClass.STICK_RIGHT) {
                            textView5.setText("Direction : Right");
                        } else if (direction == JoyStickClass.STICK_DOWNRIGHT) {
                            textView5.setText("Direction : Down Right");
                        } else if (direction == JoyStickClass.STICK_DOWN) {
                            textView5.setText("Direction : Down");
                        } else if (direction == JoyStickClass.STICK_DOWNLEFT) {
                            textView5.setText("Direction : Down Left");
                        } else if (direction == JoyStickClass.STICK_LEFT) {
                            textView5.setText("Direction : Left");
                        } else if (direction == JoyStickClass.STICK_UPLEFT) {
                            textView5.setText("Direction : Up Left");
                        } else if (direction == JoyStickClass.STICK_NONE) {
                            textView5.setText("Direction : Center");
                        }
                    } else if (arg1.getAction() == MotionEvent.ACTION_UP) {

                        textView3.setText("Angle :");
                        textView4.setText("Distance :");
                        textView5.setText("Direction :");
                    }


                    try {
                        donneEnvoiJSONPortrait.put("mode", "2"); //mode 0 pour landscape
                        donneEnvoiJSONPortrait.put("angle", anglePortrait); //vitesse moteur de gauche
                        donneEnvoiJSONPortrait.put("vitesse", vitessePortrait); //vitesse moteur de gauche
                    } catch (JSONException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }

                    String donneJsonToString = donneEnvoiJSONPortrait.toString(); // convertie le JSON en string pour l'envoyer
                    socketPortrait.sendMessage(donneJsonToString);
                    return true;
                    }
                });

        }


    }

    public void aide(View view){
        Intent intent = new Intent(this, AideActivity.class);
        startActivity(intent);

    }
    public void config(View view){
        Intent intent = new Intent(this, configActivity.class);
        startActivity(intent);

    }


    @Override
    public void onMessageReceived(String message) {


    }
}
