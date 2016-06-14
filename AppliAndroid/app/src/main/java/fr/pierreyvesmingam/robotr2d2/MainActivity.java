package fr.pierreyvesmingam.robotr2d2;

import android.content.Context;
import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
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

import com.afollestad.materialdialogs.DialogAction;
import com.afollestad.materialdialogs.MaterialDialog;

import java.net.ServerSocket;
import java.net.Socket;

import fr.pierreyvesmingam.robotr2d2.helper.RobotMoveHelper;
import rx.subscriptions.CompositeSubscription;

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
    private String mVitesseG, mVitesseD, mValAccel;
    private Serveur mServer;
    private Client mClient;
    private Socket mSocket;
    private ServerSocket mServerSocket;
    private CompositeSubscription mCompositeSubscription;

    /*
    * ************************************************************************
    * UI PROPERTIES
    * ************************************************************************
    */
    private RelativeLayout mPortraitJoystickLayout, mRightLandscapeJoystickLayout, mLeftLandscapeJoystickLayout, mRootView;
    private ImageView mImageJoystick, mImageBorder;
    private TextView mAngleTextView, mLeftSpeedTextView, mProblemTextView, mRightSpeedTextView, mSpeedTextView, mBbatteryState;
    private Button mConnexionButton, mBreakButton;

    private JoyStickClass mPortraitJoystick, mRightLandscapeJoystick, mLeftLandscapeJoystick;

    /*
    * ************************************************************************
    * STARTER METHOD
    * ************************************************************************
    */
    public static void start(Context context) {
        Intent starter = new Intent(context, MainActivity.class);
        context.startActivity(starter);
    }

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

    @Override
    protected void onPause() {
        stopClientAndServeur();
        super.onPause();
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
        AideActivity.start(this);
    }

    public void startConfigActivity(View view) {
        configActivity.start(this);
    }

    /*
    * ************************************************************************
    * PRIVATE METHODS
    * ************************************************************************
    */
    private void initData() {
        findAndInitViews();
        startClientAndServeur();
        MainActivity.IS_LANDSCAPE = getResources().getBoolean(R.bool.isLandscape);
    }

    private void startClientAndServeur() {
        mClient = RobotMoveHelper.robotConnection(mClient, MainActivity.this);
        mServer = new Serveur();
        mServer.startServeur();
        mServer.addServeurListener(MainActivity.this);
    }

    private void showErrorDialog() {
        new MaterialDialog.Builder(this)
                .title(R.string.connection_error_title)
                .content(R.string.connection_error_content)
                .neutralText(R.string.connection_error_button)
                .onNeutral(new MaterialDialog.SingleButtonCallback() {
                    @Override
                    public void onClick(@NonNull MaterialDialog dialog, @NonNull DialogAction which) {
                        finish();
                    }
                })
                .show();
    }

    private void stopClientAndServeur() {
        if (mClient != null) {
            RobotMoveHelper.robotDeconnection(mClient, getApplicationContext());
        }
    }

    private void initUI() {
        //boolean mega = false; // FIXME:: this variable is never used
        mConnexionButton.setText(R.string.disconnection);
        mBreakButton.setOnClickListener(this);
        mConnexionButton.setOnClickListener(this);
        if (MainActivity.IS_LANDSCAPE) {
            initUIForLandscape();
        } else {
            initUIForPortrait();
        }
    }

    private void findAndInitViews() {
        mAngleTextView = (TextView) findViewById(R.id.angleTextView);
        mLeftSpeedTextView = (TextView) findViewById(R.id.leftSpeedTextView);
        mRightSpeedTextView = (TextView) findViewById(R.id.rightSpeedTextView);
        mProblemTextView = (TextView) findViewById(R.id.problemTextView);
        mRootView = (RelativeLayout) findViewById(R.id.rootView);
        mPortraitJoystickLayout = (RelativeLayout) findViewById(R.id.portraitJoystickLayout);
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
        if (motionEvent.getAction() == motionEvent.ACTION_UP) {
            RobotMoveHelper.stopMotors(mClient);
        } else {
            RobotMoveHelper.launchMotorsWithModeZero(mClient, mVitesseD, mVitesseG);
        }
    }

    private void onTouchRightLanscapeJoystick(@NonNull final MotionEvent motionEvent) {
        mRightLandscapeJoystick.drawStick(motionEvent);
        int speed = Math.round(mRightLandscapeJoystick.getDistance());

        mVitesseD = RobotMoveHelper.motorSpeedCalcul(speed);
        mRightSpeedTextView.setText(String.format(getString(R.string.right_speed_with_value), mVitesseD));
        if (motionEvent.getAction() == motionEvent.ACTION_UP) {
            RobotMoveHelper.stopMotors(mClient);
        } else {
            RobotMoveHelper.launchMotorsWithModeZero(mClient, mVitesseD, mVitesseG);
        }
    }

    private void initUIForPortrait() {
        //portrait
        //joystick principale en mode portrait
        mPortraitJoystick = new JoyStickClass(this, mPortraitJoystickLayout, R.drawable.rouge);
        mPortraitJoystick.setStickSize(150, 150);
        //mPortraitJoystick.setStickAlpha(50);
        mPortraitJoystick.setOffset(130);
        mPortraitJoystick.setMinimumDistance(50);

        mPortraitJoystickLayout.setOnTouchListener(this);
    }

    private void onTouchPortraitJoystick(@NonNull final MotionEvent motionEvent) {

        mPortraitJoystick.drawStick(motionEvent);
        final int angle = Math.round(mPortraitJoystick.getAngle());
        final String angleString = String.valueOf(angle);

        final int speed = Math.round(mPortraitJoystick.getDistance());
        final String speedString = RobotMoveHelper.motorSpeedCalcul(speed);

        mAngleTextView.setText(String.format(getString(R.string.angle_with_value), angleString));
        mLeftSpeedTextView.setText(String.format(getString(R.string.distance_with_value), speedString));
        if (motionEvent.getAction() == motionEvent.ACTION_UP) {
            RobotMoveHelper.stopMotors(mClient);
        } else {
            RobotMoveHelper.launchMotorsWithModeTwo(mClient, angleString, speedString);
        }
    }

    private void onClickConnexionButton() {
        finish();
    }
}
