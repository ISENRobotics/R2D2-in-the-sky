package fr.pierreyvesmingam.robotr2d2;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class LuncherActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_luncher);
    }

    public void mainacti(View view){
        Intent intent1 = new Intent(this, MainActivity.class);
        startActivity(intent1);

    }
}
