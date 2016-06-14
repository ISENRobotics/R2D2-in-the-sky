package fr.pierreyvesmingam.robotr2d2;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;

public class LauncherActivity extends AppCompatActivity {

    /*
    * ************************************************************************
    * LIFE CYCLE METHODS
    * ************************************************************************
    */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_luncher);
    }

    /*
    * ************************************************************************
    * USER INTERACTION METHODS
    * ************************************************************************
    */
    public void launchRobotActivity(View view) {
        MainActivity.start(this);
    }
}
