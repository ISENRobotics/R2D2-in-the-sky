package fr.pierreyvesmingam.robotr2d2;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class AideActivity extends AppCompatActivity {

    /*
    * ************************************************************************
    * UI PROPERTIES
    * ************************************************************************
    */
    private TextView response;
    private EditText editTextAddress, editTextPort;
    private Button buttonConnect;

    /*
    * ************************************************************************
    * STARTER METHODS
    * ************************************************************************
    */
    public static void start(Context context) {
        Intent starter = new Intent(context, AideActivity.class);
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
        setContentView(R.layout.activity_aide);

        editTextAddress = (EditText) findViewById(R.id.addressEditText);
        editTextPort = (EditText) findViewById(R.id.portEditText);
        buttonConnect = (Button) findViewById(R.id.connectButton);
        response = (TextView) findViewById(R.id.responseTextView);
    }

    /*
    * ************************************************************************
    * PUBLIC METHODS
    * ************************************************************************
    */
    public void retour(View view) {
        finish();
    }
}
