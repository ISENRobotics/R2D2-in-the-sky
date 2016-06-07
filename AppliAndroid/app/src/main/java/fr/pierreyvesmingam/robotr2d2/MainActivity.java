package fr.pierreyvesmingam.robotr2d2;

import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.SystemClock;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.OnTouchListener;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.Calendar;

public class MainActivity extends AppCompatActivity implements Client.ClientListener, Serveur.ServerListener, View.OnClickListener {

    /*
    * ************************************************************************
    * STATIC PROPERTIES
    * ************************************************************************
    */
    public static boolean IS_LANDSCAPE = false;
    private final JSONObject donneEnvoiJSON = new JSONObject();
    private final JSONObject donneEnvoiJSONPortrait = new JSONObject();
    private final JSONObject deconexionJSON = new JSONObject();
    /*
    * ************************************************************************
    * DATA PROPERTIES
    * ************************************************************************
    */
    private float intVitesseG, intVitesseD;
    private String vitesseG, vitesseD, anglePortrait, deconexionJSONtoString, millisToString, donneJsonToString, vitesseP, tempsmm, vitessePortrait, valAccel;
    private Integer intVitesseP, intAngle, appui;
    private boolean etatServeur, mIsConnected, isFirstRightJoystickInit, isFirstLeftJoystickInit, ListenerOrNot1, AppuiConnexionPortrait, AppuiConnexionPaysage;
    private Serveur socketStream, serveur;
    private Client client, socketLandscape;

    /*
    * ************************************************************************
    * UI PROPERTIES
    * ************************************************************************
    */
    private RelativeLayout mLayoutPortraitJoystick, mLayoutLandscapeRightJoystick, mLayoutLandscapeLeftJoystick, mRootView;
    private ImageView image_joystick, image_border;
    private TextView mAngleTextView, mLeftSpeedTextView, mLeftDirectionTextView, mProblemTextView, mRightSpeedTextView, mRightDirectionTextView, mSpeedTextView, mBbatteryState;
    private Button connexionButton, mBreakButton;

    private JoyStickClass js, js2, js3;

    /*
    * ************************************************************************
    * LIFE CYCLE METHODS
    * ************************************************************************
    */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initData();
        initUI();
    }

    //retour du thread serveur ici
    @Override
    public void onVideoRecieved(String message) {
        final String dataStream = message;
        System.out.println("Le string recu du serveur est : " + dataStream);
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                mRootView.setBackground(Drawable.createFromPath("Informations serveur:" + dataStream));

            }
        });
    }

    //retour du thread client ici
    @Override
    public void onMessageReceived(String message) {
        final String data = message;
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                System.out.println("Dans le MainActivity" + data);
                mProblemTextView.setText(data);
            }
        });
    }

    /*
    * ************************************************************************
    * USER INTERACTION METHODS
    * ************************************************************************
    */
    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.connexionButton:
                onClickConnexionButton();
                break;
            case R.id.breakButton:
                onClickBreackButton();
                break;
        }
    }

    public void startHelpActivity(View view) {
        Intent intent = new Intent(this, AideActivity.class);
        startActivity(intent);
    }

    public void startConfigActivity(View view) {
        Intent intent = new Intent(this, configActivity.class);
        startActivity(intent);
    }

    /*
    * ************************************************************************
    * PRIVATE METHODS
    * ************************************************************************
    */
    private void initData() {
        initClient();
        findAndInitViews();
        MainActivity.IS_LANDSCAPE = getResources().getBoolean(R.bool.isLandscape);
    }

    private void initUI() {
        boolean mega = false; // FIXME:: this variable is never used
        mBreakButton.setOnClickListener(this);
        connexionButton.setOnClickListener(this);
        if (MainActivity.IS_LANDSCAPE) {
            initUIForLandscape();
        } else {
            initUIForPortrait();
        }
    }

    private void initClient() {
        if (client == null) {
            client = new Client();
            client.addClientListener(this);
            socketLandscape = client;
        }
    }

    private void findAndInitViews() {
        mAngleTextView = (TextView) findViewById(R.id.angleTextView);
        mLeftSpeedTextView = (TextView) findViewById(R.id.leftSpeedTextView);
        mLeftDirectionTextView = (TextView) findViewById(R.id.leftDirectionTextView);
        mRightSpeedTextView = (TextView) findViewById(R.id.rightSpeedTextView);
        mRightDirectionTextView = (TextView) findViewById(R.id.rightDirectionTextView);
        mProblemTextView = (TextView) findViewById(R.id.problemTextView);
        mRootView = (RelativeLayout) findViewById(R.id.rootView);
        mLayoutPortraitJoystick = (RelativeLayout) findViewById(R.id.layoutPortraitJoystick);
        mLayoutLandscapeRightJoystick = (RelativeLayout) findViewById(R.id.layoutLandscapeRightJoystick);
        mLayoutLandscapeLeftJoystick = (RelativeLayout) findViewById(R.id.layoutLandscapeLeftJoystick);

        mBreakButton = (Button) findViewById(R.id.breakButton);
        connexionButton = (Button) findViewById(R.id.connexionButton);
    }

    private void onClickBreackButton() {
        // Perform action on click
        System.out.println("Arret d'urgence");
        try {
            vitesseD = "0000";
            vitesseG = "0000";
            Calendar cal = Calendar.getInstance();
            millisToString = String.valueOf(cal.getTimeInMillis());
            donneEnvoiJSON.put("mode", "8"); //mode 0 pour landscape
            donneEnvoiJSON.put("vitesseG", vitesseG); //vitesse moteur de gauche
            donneEnvoiJSON.put("vitesseD", vitesseD); //vitesse moteur de gauche
            donneEnvoiJSON.put("temps", millisToString); //vitesse moteur de gauche
        } catch (JSONException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        donneJsonToString = donneEnvoiJSON.toString(); // convertie le JSON en string pour l'envoyer
        socketLandscape.sendMessage(donneJsonToString);
    }

    private void initUIForLandscape() {
        //Landscape
        //joystick 1, a gauche sur vu paysage
        js3 = new JoyStickClass(getApplicationContext(), mLayoutLandscapeLeftJoystick, R.drawable.rouge);
        js3.setStickSize(150, 150);
        js3.setLayoutSize(500, 500);
        js3.setLayoutAlpha(150);
        js3.setStickAlpha(100);
        js3.setOffset(90);
        js3.setMinimumDistance(0);

        mLayoutLandscapeLeftJoystick.setOnTouchListener(new OnTouchListener() {
            public boolean onTouch(View arg7, MotionEvent arg2) {
                js3.drawStick(arg2);
                isFirstLeftJoystickInit = false;
                // ListenerOrNot1 = true;
                if (arg2.getAction() == MotionEvent.ACTION_DOWN
                        || arg2.getAction() == MotionEvent.ACTION_MOVE) {
                    intVitesseG = Math.round(js3.getDistance());
                    vitesseG = String.valueOf(intVitesseG);
                    mLeftSpeedTextView.setText("Vitesse G : " + vitesseG);

                    //mise en forme pour le JSON des vitesse
                    int direction = js3.get8Direction();
                    if (direction == JoyStickClass.STICK_UP) {
                        mLeftDirectionTextView.setText("Direction G : Up");
                    } else if (direction == JoyStickClass.STICK_UPRIGHT) {
                        mLeftDirectionTextView.setText("Direction G: Up");
                    } else if (direction == JoyStickClass.STICK_RIGHT) {
                        mLeftDirectionTextView.setText("Direction G: Center");
                    } else if (direction == JoyStickClass.STICK_DOWNRIGHT) {
                        mLeftDirectionTextView.setText("Direction G: Down");
                    } else if (direction == JoyStickClass.STICK_DOWN) {
                        mLeftDirectionTextView.setText("Direction G: Down");
                    } else if (direction == JoyStickClass.STICK_DOWNLEFT) {
                        mLeftDirectionTextView.setText("Direction G: Down");
                    } else if (direction == JoyStickClass.STICK_LEFT) {
                        mLeftDirectionTextView.setText("Direction G: Center");
                    } else if (direction == JoyStickClass.STICK_UPLEFT) {
                        mLeftDirectionTextView.setText("Direction G: Up");
                    } else if (direction == JoyStickClass.STICK_NONE) {
                        mLeftDirectionTextView.setText("Direction G: Center");
                    }
                } else if (arg2.getAction() == MotionEvent.ACTION_UP) {


                    mLeftSpeedTextView.setText("Distance G:");
                    mLeftDirectionTextView.setText("Direction G:");
                }
                vitesseG = Integer.toString((Math.round(intVitesseG / 100 * 127)));
                intVitesseG = Math.round(intVitesseG / 100 * 127);
                boolean megaG = false;
                if (intVitesseG < 0) {
                    megaG = true;
                } else if (intVitesseG == 0) {
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

                appui = 1;

                if (isFirstRightJoystickInit) { // FIXME : this is not a right way to init the value
                    vitesseD = "0000";
                }
                try {
                    Calendar cal = Calendar.getInstance();
                    millisToString = new String(String.valueOf(cal.getTimeInMillis()));
                    donneEnvoiJSON.put("mode", "0"); //mode 0 pour landscape
                    donneEnvoiJSON.put("vitesseG", vitesseG); //vitesse moteur de gauche
                    donneEnvoiJSON.put("vitesseD", vitesseD); //vitesse moteur de gauche
                    donneEnvoiJSON.put("temps", millisToString);
                } catch (JSONException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

                String donneJsonToString = donneEnvoiJSON.toString(); // convertie le JSON en string pour l'envoyer
                socketLandscape.sendMessage(donneJsonToString);

                appui = 0;
                return true;
            }
        });

        //joystick 2, a droite sur vu paysage
        js2 = new JoyStickClass(this, mLayoutLandscapeRightJoystick, R.drawable.rouge);
        js2.setStickSize(150, 150);
        js2.setLayoutSize(500, 500);
        js2.setLayoutAlpha(150);
        js2.setStickAlpha(100);
        js2.setOffset(90);
        js2.setMinimumDistance(0);

        mLayoutLandscapeRightJoystick.setOnTouchListener(new OnTouchListener() {
            public boolean onTouch(View arg8, MotionEvent arg1) {
                js2.drawStick(arg1);
                isFirstRightJoystickInit = false;
                if (arg1.getAction() == MotionEvent.ACTION_DOWN
                        || arg1.getAction() == MotionEvent.ACTION_MOVE) {

                    intVitesseD = new Float(Math.round(js2.getDistance()));
                    vitesseD = new String(String.valueOf(intVitesseD));


                    mRightSpeedTextView.setText("Vitesse D: " + vitesseD);

                    int direction = js2.get8Direction();
                    if (direction == JoyStickClass.STICK_UP) {
                        mRightDirectionTextView.setText("Direction D: Up");
                    } else if (direction == JoyStickClass.STICK_UPRIGHT) {
                        mRightDirectionTextView.setText("Direction D: Up");
                    } else if (direction == JoyStickClass.STICK_RIGHT) {
                        mRightDirectionTextView.setText("Direction D: Center");
                    } else if (direction == JoyStickClass.STICK_DOWNRIGHT) {
                        mRightDirectionTextView.setText("Direction D: Down");
                    } else if (direction == JoyStickClass.STICK_DOWN) {
                        mRightDirectionTextView.setText("Direction D: Down");
                    } else if (direction == JoyStickClass.STICK_DOWNLEFT) {
                        mRightDirectionTextView.setText("Direction D: Down");
                    } else if (direction == JoyStickClass.STICK_LEFT) {
                        mRightDirectionTextView.setText("Direction D: Center");
                    } else if (direction == JoyStickClass.STICK_UPLEFT) {
                        mRightDirectionTextView.setText("Direction D: Up");
                    } else if (direction == JoyStickClass.STICK_NONE) {
                        mRightDirectionTextView.setText("Direction D: Center");
                    }
                } else if (arg1.getAction() == MotionEvent.ACTION_UP) {

                    mRightSpeedTextView.setText("Distance D:");
                    mRightDirectionTextView.setText("Direction D:");
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

                System.out.println("LE TEMPS EST PRESENT MGL" + millisToString);
                appui = 2;

                if (isFirstLeftJoystickInit) {
                    vitesseG = "0000";
                }
                try {
                    Calendar cal = Calendar.getInstance();
                    millisToString = String.valueOf(cal.getTimeInMillis());
                    donneEnvoiJSON.put("mode", "0"); //mode 0 pour landscape
                    donneEnvoiJSON.put("vitesseG", vitesseG); //vitesse moteur de gauche
                    donneEnvoiJSON.put("vitesseD", vitesseD); //vitesse moteur de gauche
                    donneEnvoiJSON.put("temps", millisToString);
                } catch (JSONException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

                donneJsonToString = donneEnvoiJSON.toString(); // convertie le JSON en string pour l'envoyer
                socketLandscape.sendMessage(donneJsonToString);
                appui = 0;
                return true;
            }
        });

    }

    private void initUIForPortrait() {
        //portrait
        //joystick principale en mode portrait
        js = new JoyStickClass(this, mLayoutPortraitJoystick, R.drawable.rouge);
        js.setStickSize(150, 150);
        js.setLayoutSize(500, 500);
        js.setLayoutAlpha(150);
        js.setStickAlpha(100);
        js.setOffset(90);
        js.setMinimumDistance(50);

        mLayoutPortraitJoystick.setOnTouchListener(new OnTouchListener() {
            public boolean onTouch(View arg0, MotionEvent arg3) {
                //AppuiConnexionPortrait = true;
                js.drawStick(arg3);
                if (arg3.getAction() == MotionEvent.ACTION_DOWN
                        || arg3.getAction() == MotionEvent.ACTION_MOVE) {

                    intAngle = Math.round(js.getAngle());
                    anglePortrait = String.valueOf(intAngle);
                    vitesseP = String.valueOf(Math.round(js.getDistance()));
                    intVitesseP = Math.round(js.getDistance());

                    mAngleTextView.setText("Angle : " + anglePortrait);
                    mLeftSpeedTextView.setText("Distance : " + vitesseP);

                    int direction = js.get8Direction();
                    if (direction == JoyStickClass.STICK_UP) {
                        mLeftDirectionTextView.setText("Direction : Up");
                    } else if (direction == JoyStickClass.STICK_UPRIGHT) {
                        mLeftDirectionTextView.setText("Direction : Up Right");
                    } else if (direction == JoyStickClass.STICK_RIGHT) {
                        mLeftDirectionTextView.setText("Direction : Right");
                    } else if (direction == JoyStickClass.STICK_DOWNRIGHT) {
                        mLeftDirectionTextView.setText("Direction : Down Right");
                    } else if (direction == JoyStickClass.STICK_DOWN) {
                        mLeftDirectionTextView.setText("Direction : Down");
                    } else if (direction == JoyStickClass.STICK_DOWNLEFT) {
                        mLeftDirectionTextView.setText("Direction : Down Left");
                    } else if (direction == JoyStickClass.STICK_LEFT) {
                        mLeftDirectionTextView.setText("Direction : Left");
                    } else if (direction == JoyStickClass.STICK_UPLEFT) {
                        mLeftDirectionTextView.setText("Direction : Up Left");
                    } else if (direction == JoyStickClass.STICK_NONE) {
                        mLeftDirectionTextView.setText("Direction : Center");
                    }
                } else if (arg3.getAction() == MotionEvent.ACTION_UP) {

                    mAngleTextView.setText("Angle :");
                    mLeftSpeedTextView.setText("Distance :");
                    mLeftDirectionTextView.setText("Direction :");
                }

                boolean megaPortrait = false;
                vitesseP = Integer.toString((Math.round(intVitesseP / (float) 100 * (float) 127)));
                intVitesseP = Math.round(intVitesseP / (float) 100 * (float) 127);
                if (intVitesseP < 0) {
                    megaPortrait = true;
                } else if (intVitesseP == 0) {
                    vitesseP = "0000";
                }
                if (megaPortrait) {

                    if (vitesseP.length() == 2) {
                        vitesseP = "-00" + Integer.toString(Math.abs(Math.round(intVitesseP)));
                    }
                    if (vitesseP.length() == 3) {
                        vitesseP = "-0" + Integer.toString(Math.abs(Math.round(intVitesseP)));
                        System.out.println("Are You Here My Brother Friend ?");
                    }
                } else {
                    if (vitesseP.length() == 1) {
                        vitesseP = "000" + vitesseP;
                    } else if (vitesseP.length() == 2) {
                        vitesseP = "00" + vitesseP;
                    } else if (vitesseP.length() == 3) {
                        vitesseP = "0" + vitesseP;
                    }
                }
                try {
                    Calendar cal = Calendar.getInstance();
                    millisToString = String.valueOf(cal.getTimeInMillis());
                    donneEnvoiJSONPortrait.put("mode", "2"); //mode 0 pour landscape
                    donneEnvoiJSONPortrait.put("angle", anglePortrait); //vitesse moteur de gauche
                    donneEnvoiJSONPortrait.put("vitesse", vitesseP); //vitesse moteur de gauche
                    donneEnvoiJSONPortrait.put("temps", millisToString);
                } catch (JSONException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }

                donneJsonToString = donneEnvoiJSONPortrait.toString(); // convertie le JSON en string pour l'envoyer
                socketLandscape.sendMessage(donneJsonToString);
                return true;
            }
        });
    }

    private void onClickConnexionButton() {
        // Perform action on click
        if (!mIsConnected) {
            Log.d("CONNEXION_BUTTON", "Je suis dans le bouton connexion");
            AppuiConnexionPaysage = true;
            try {
                socketLandscape.startClient();
                if (!etatServeur) {
                    etatServeur = true;
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

            if (socketLandscape.getConnxion() == 0) {
                Toast.makeText(getApplicationContext(), "Connected", Toast.LENGTH_SHORT).show();
            } else if (socketLandscape.getConnxion() == 1) {
                Toast.makeText(getApplicationContext(), "Connection refused", Toast.LENGTH_SHORT).show();
            }
            connexionButton.setText("Disconnect");
            connexionButton.setBackgroundColor(0xfff00000);
            mIsConnected = true;
        } else {
            Log.d("CONNEXION_BUTTON", "Je suis dans le bouton Deconnexion");
            AppuiConnexionPaysage = true;

            try {
                deconexionJSON.put("connexion", "false"); //vitesse moteur de gauche
            } catch (JSONException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            deconexionJSONtoString = deconexionJSON.toString(); // convertie le JSON en string pour l'envoyer
            socketLandscape.sendMessage(deconexionJSONtoString);
            SystemClock.sleep(100);
            socketLandscape.stopClient();
            //socketStream.stopServeur();
            createNewClient();
            connexionButton.setText("Connexion");
            connexionButton.setBackgroundColor(0xff00c700);
        }
    }
    private void createNewClient() {
        socketLandscape = new Client();
        mIsConnected = true;
    }
}
