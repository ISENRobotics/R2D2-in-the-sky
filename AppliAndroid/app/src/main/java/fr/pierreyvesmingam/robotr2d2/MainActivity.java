package fr.pierreyvesmingam.robotr2d2;

import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.SystemClock;
import android.support.annotation.NonNull;
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

import fr.pierreyvesmingam.robotr2d2.helper.RobotMoveHelper;

public class MainActivity extends AppCompatActivity implements Client.ClientListener, Serveur.ServerListener, View.OnClickListener, OnTouchListener {

    /*
    * ************************************************************************
    * STATIC PROPERTIES
    * ************************************************************************
    */
    public static boolean IS_LANDSCAPE = false;
    /*
    * ************************************************************************
    * DATA PROPERTIES
    * ************************************************************************
    */
    private final JSONObject mDeconnectionJSON = new JSONObject();

    private String mVitesseG, mVitesseD, mAnglePortrait, mMillisToString, mDonneJsonToString, mTempsmm, mVitessePortrait, mValAccel;
    private boolean mIsConnected, mIsFirstRightJoystickInit, mIsFirstLeftJoystickInit, mListenerOrNot1, mPressConnectionPortrait, mPressConnectionLandscape;
    private Serveur mSocketStream, mServeur;
    private Client mClient;

    /*
    * ************************************************************************
    * UI PROPERTIES
    * ************************************************************************
    */
    private RelativeLayout mLayoutPortraitJoystick, mRightLandscapeJoystickLayout, mLeftLandscapeJoystickLayout, mRootView;
    private ImageView mImageJoystick, mImageBorder;
    private TextView mAngleTextView, mLeftSpeedTextView, mProblemTextView, mRightSpeedTextView, mSpeedTextView, mBbatteryState;
    private Button mConnexionButton, mBreakButton;

    private JoyStickClass mProtraitJoystick, mRightLandscapeJoystick, mLeftLandscapeJoystick;

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
        Log.d("VIDEO_RECIEVE", "Le string recu du serveur est : " + dataStream);
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
                Log.d("MESSAGE_RECIEVE", "Dans le MainActivity " + data);
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

    @Override
    public boolean onTouch(View view, MotionEvent motionEvent) {
        switch (view.getId()) {
            case R.id.rightLandscapeJoystickLayout:
                onTouchRightLanscapeJoystick(motionEvent);
                break;
            case R.id.leftLandscapeJoystickLayout:
                onTouchLeftLandscapeJoystick(motionEvent);
                break;
            case R.id.portraitJoystickLayout:
                onTouchPortraitJoystick(motionEvent);
                break;
        }
        return true;
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
        findAndInitViews();
        MainActivity.IS_LANDSCAPE = getResources().getBoolean(R.bool.isLandscape);
    }

    private void initUI() {
        //boolean mega = false; // FIXME:: this variable is never used
        mBreakButton.setOnClickListener(this);
        mConnexionButton.setOnClickListener(this);
        if (MainActivity.IS_LANDSCAPE) {
            initUIForLandscape();
        } else {
            initUIForPortrait();
        }
    }

    private void initClient() {
        if (mClient == null) {
            mClient = new Client();
            mClient.addClientListener(this);
        }
    }

    private void findAndInitViews() {
        mAngleTextView = (TextView) findViewById(R.id.angleTextView);
        mLeftSpeedTextView = (TextView) findViewById(R.id.leftSpeedTextView);
        mRightSpeedTextView = (TextView) findViewById(R.id.rightSpeedTextView);
        mProblemTextView = (TextView) findViewById(R.id.problemTextView);
        mRootView = (RelativeLayout) findViewById(R.id.rootView);
        mLayoutPortraitJoystick = (RelativeLayout) findViewById(R.id.portraitJoystickLayout);
        mRightLandscapeJoystickLayout = (RelativeLayout) findViewById(R.id.rightLandscapeJoystickLayout);
        mLeftLandscapeJoystickLayout = (RelativeLayout) findViewById(R.id.leftLandscapeJoystickLayout);

        mBreakButton = (Button) findViewById(R.id.breakButton);
        mConnexionButton = (Button) findViewById(R.id.connexionButton);
    }

    private void onClickBreackButton() {
        // Perform action on click
        Log.d("STOP_ROBOT", "Frein d'urgence");
        RobotMoveHelper.stopMotors(mClient);
    }

    private void initUIForLandscape() {
        //Landscape
        //joystick 1, a gauche sur vu paysage
        mLeftLandscapeJoystick = new JoyStickClass(getApplicationContext(), mLeftLandscapeJoystickLayout, R.drawable.rouge);
        mLeftLandscapeJoystick.setStickSize(150, 150);
        mLeftLandscapeJoystick.setLayoutSize(500, 500);
        mLeftLandscapeJoystick.setLayoutAlpha(150);
        mLeftLandscapeJoystick.setStickAlpha(100);
        mLeftLandscapeJoystick.setOffset(90);
        mLeftLandscapeJoystick.setMinimumDistance(0);

        mLeftLandscapeJoystickLayout.setOnTouchListener(this);

        //joystick 2, a droite sur vu paysage
        mRightLandscapeJoystick = new JoyStickClass(this, mRightLandscapeJoystickLayout, R.drawable.rouge);
        mRightLandscapeJoystick.setStickSize(150, 150);
        mRightLandscapeJoystick.setLayoutSize(500, 500);
        mRightLandscapeJoystick.setLayoutAlpha(150);
        mRightLandscapeJoystick.setStickAlpha(100);
        mRightLandscapeJoystick.setOffset(90);
        mRightLandscapeJoystick.setMinimumDistance(0);

        mRightLandscapeJoystickLayout.setOnTouchListener(this);
    }

    private void onTouchLeftLandscapeJoystick(@NonNull final MotionEvent motionEvent) {
        mLeftLandscapeJoystick.drawStick(motionEvent);
        int speed = Math.round(mLeftLandscapeJoystick.getDistance());
        mVitesseG = RobotMoveHelper.motorSpeedCalcul(speed);
        mLeftSpeedTextView.setText(String.format(getString(R.string.left_speed_with_value), mVitesseG));
        RobotMoveHelper.launchMotorsWithModeZero(mClient, mVitesseD, mVitesseG);
    }

    private void onTouchRightLanscapeJoystick(@NonNull final MotionEvent motionEvent) {
        mRightLandscapeJoystick.drawStick(motionEvent);
        int speed = Math.round(mRightLandscapeJoystick.getDistance());
        mVitesseD = RobotMoveHelper.motorSpeedCalcul(speed);
        mRightSpeedTextView.setText(String.format(getString(R.string.right_speed_with_value), mVitesseD));
        RobotMoveHelper.launchMotorsWithModeZero(mClient, mVitesseD, mVitesseG);
    }

    private void initUIForPortrait() {
        //portrait
        //joystick principale en mode portrait
        mProtraitJoystick = new JoyStickClass(this, mLayoutPortraitJoystick, R.drawable.rouge);
        mProtraitJoystick.setStickSize(150, 150);
        mProtraitJoystick.setLayoutSize(500, 500);
        mProtraitJoystick.setLayoutAlpha(150);
        mProtraitJoystick.setStickAlpha(100);
        mProtraitJoystick.setOffset(90);
        mProtraitJoystick.setMinimumDistance(50);

        mLayoutPortraitJoystick.setOnTouchListener(this);
    }

    private void onTouchPortraitJoystick(@NonNull final MotionEvent motionEvent) {
        //mPressConnectionPortrait = true;
        String speedString;
        int speed = 0;
        mProtraitJoystick.drawStick(motionEvent);
        if (motionEvent.getAction() == MotionEvent.ACTION_DOWN
                || motionEvent.getAction() == MotionEvent.ACTION_MOVE) {

            final int angle = Math.round(mProtraitJoystick.getAngle());
            mAnglePortrait = String.valueOf(angle);
            speedString = String.valueOf(Math.round(mProtraitJoystick.getDistance()));
            speed = Math.round(mProtraitJoystick.getDistance());

            mAngleTextView.setText(String.format(getString(R.string.angle_with_value), mAnglePortrait));
            mLeftSpeedTextView.setText(String.format(getString(R.string.distance_with_value), speedString));

        } else if (motionEvent.getAction() == MotionEvent.ACTION_UP) {
            mAngleTextView.setText(R.string.angle);
            mLeftSpeedTextView.setText(R.string.distance);
        }

        speedString = RobotMoveHelper.motorSpeedCalcul(speed);
        RobotMoveHelper.launchMotorsWithModeTwo(mClient, mAnglePortrait, speedString);
    }

    private void onClickConnexionButton() {
        // Perform action on click
        if (!mIsConnected) {
            initClient();
            Log.d("CONNEXION_BUTTON", "Je suis dans le bouton connexion");
            mPressConnectionLandscape = true;
            try {
                mClient.startClient();
            } catch (IOException e) {
                e.printStackTrace();
            }

            if (!mClient.nullableSocket()) {
                if (mClient.socketIsConnected()) {
                    mIsConnected = true;
                    Toast.makeText(getApplicationContext(), R.string.connected, Toast.LENGTH_SHORT).show();
                    mConnexionButton.setText(R.string.disconnection);
                    mConnexionButton.setBackgroundColor(0xfff00000);
                } else {
                    Toast.makeText(getApplicationContext(), R.string.connection_refused, Toast.LENGTH_SHORT).show();
                    mClient = null;
                }
            } else {
                Toast.makeText(getApplicationContext(), R.string.connection_refused, Toast.LENGTH_SHORT).show();
            }
        } else {
            Log.d("CONNEXION_BUTTON", "Je suis dans le bouton Deconnexion");
            mPressConnectionLandscape = false;

            try {
                mDeconnectionJSON.put("connexion", "false"); //vitesse moteur de gauche
            } catch (JSONException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
            final String deconexionJSONtoString = mDeconnectionJSON.toString(); // convertie le JSON en string pour l'envoyer
            mClient.sendMessage(deconexionJSONtoString);
            SystemClock.sleep(100);
            mClient.stopClient();
            //mSocketStream.stopServeur();
            mConnexionButton.setText(R.string.connection);
            mConnexionButton.setBackgroundColor(0xff00c700);
            mIsConnected = false;
            mClient = null;
        }
    }
}
