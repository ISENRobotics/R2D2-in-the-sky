package fr.pierreyvesmingam.robotr2d2;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

public class configActivity extends AppCompatActivity implements SeekBar.OnSeekBarChangeListener, View.OnClickListener {

    /*
    * ************************************************************************
    * DATA PROPERTIES
    * ************************************************************************
    */
    private int speed = 0;
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
    * STARTER METHOD
    * ************************************************************************
    */
    public static void start(Context context) {
        Intent starter = new Intent(context, configActivity.class);
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
        setContentView(R.layout.activity_config2);
        initUI();
    }

    /*
    * ************************************************************************
    * PUBLIC METHODS
    * ************************************************************************
    */
    public Integer getValAccle() {
        return speed;
    }

    public void retour(View view) {
        /*Intent i = new Intent(this, MainActivity.class);
        String speedString = Integer.toString(this.speed);
        i.putExtra("speed", speedString);
        System.out.println("Dans la fonction retour" + Integer.toString(this.speed));
        startActivity(i);*/
        finish();
    }


    /*
    * ************************************************************************
    * IMPLEMENTS METHODS
    * ************************************************************************
    */
    @Override
    public void onClick(View arg0) {
              /*  Client myClient = new Client(editTextAddress.getText()
                        .toString(), Integer.parseInt(editTextPort
                        .getText().toString()), response);
                myClient.execute();*/
    }

    @Override
    public void onProgressChanged(SeekBar seekBar, int progress, boolean b) {
        speed = progress + 1;
    }

    @Override
    public void onStartTrackingTouch(SeekBar seekBar) {
        // TODO Auto-generated method stub
    }

    @Override
    public void onStopTrackingTouch(SeekBar seekBar) {
        Toast.makeText(configActivity.this, "Accélération:" + speed,
                Toast.LENGTH_SHORT).show();
    }

    /*
    * ************************************************************************
    * PRIVATE METHODS
    * ************************************************************************
    */
    private void initUI() {
        //code pour la seekbar
        final SeekBar accel = (SeekBar) findViewById(R.id.seek1);
        if (accel != null) {
            accel.setOnSeekBarChangeListener(this);
        }

        editTextAddress = (EditText) findViewById(R.id.addressEditText);
        editTextPort = (EditText) findViewById(R.id.portEditText);
        buttonConnect = (Button) findViewById(R.id.connectButton);

        response = (TextView) findViewById(R.id.responseTextView);

        buttonConnect.setOnClickListener(this);
    }
}
