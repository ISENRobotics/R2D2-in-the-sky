package fr.pierreyvesmingam.robotr2d2;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Html;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class AideActivity extends AppCompatActivity {

    TextView response;
    EditText editTextAddress, editTextPort;
    Button buttonConnect;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_aide);

        editTextAddress = (EditText) findViewById(R.id.addressEditText);
        editTextPort = (EditText) findViewById(R.id.portEditText);
        buttonConnect = (Button) findViewById(R.id.connectButton);

        response = (TextView) findViewById(R.id.responseTextView);

    }

    public void retour(View view){
        finish();

    }
}
