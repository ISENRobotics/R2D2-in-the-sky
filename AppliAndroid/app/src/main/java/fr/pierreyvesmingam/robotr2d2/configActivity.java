package fr.pierreyvesmingam.robotr2d2;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

public class configActivity extends AppCompatActivity {

    TextView response;
    EditText editTextAddress, editTextPort;
    Button buttonConnect;
    Integer speed;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_config2);

        //code pour la seekbar
        SeekBar accel = (SeekBar) findViewById(R.id.seek1);
        accel.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            int speed = 0;

            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                speed = progress + 1;
            }

            public void onStartTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }

            public void onStopTrackingTouch(SeekBar seekBar) {
                Toast.makeText(configActivity.this, "Accélération:" + speed,
                        Toast.LENGTH_SHORT).show();
            }
        });


        //code pour la sauvegarde de l'adresse IP
        editTextAddress = (EditText) findViewById(R.id.addressEditText);
        editTextPort = (EditText) findViewById(R.id.portEditText);
        buttonConnect = (Button) findViewById(R.id.connectButton);

        response = (TextView) findViewById(R.id.responseTextView);

        buttonConnect.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View arg0) {
              /*  Client myClient = new Client(editTextAddress.getText()
                        .toString(), Integer.parseInt(editTextPort
                        .getText().toString()), response);
                myClient.execute();*/
            }
        });
    }


    public Integer getValAccle()
    {

        return speed;
    }

    public void retour(View view){

        /*Intent i = new Intent(this, MainActivity.class);
        String speedString = Integer.toString(this.speed);
        i.putExtra("speed", speedString);
        System.out.println("Dans la fonction retour" + Integer.toString(this.speed));
        startActivity(i);*/
        finish();

    }
}
