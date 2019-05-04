package com.example.ebias;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.TextView;

import org.w3c.dom.Text;

public class MainActivity extends AppCompatActivity {

    private String mUserId;
    private String mServer;
    private String mAlgo;
    private String mUserIdIdx;
    private String mServerIdx;
    private String mAlgoIdx;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Intent t= getIntent();
        mUserId = t.getStringExtra("user");
        mAlgo = t.getStringExtra("algo");
        mServer = t.getStringExtra("server");
        mUserIdIdx = t.getStringExtra("userIdx");
        mAlgoIdx = t.getStringExtra("algoIdx");
        mServerIdx = t.getStringExtra("serverIdx");
        TextView serverID = (TextView) findViewById(R.id.rc12);
        TextView algoID = (TextView) findViewById(R.id.rc22);
        serverID.setText(mServer);
        algoID.setText(mAlgo);
        if(mServerIdx == "0"){
            TextView cptime = (TextView) findViewById(R.id.rc32);
            cptime.setText("24 ms");
        }
        if(mServerIdx == "1"){
            TextView cptime = (TextView) findViewById(R.id.rc32);
            cptime.setText("216 ms");
        }
        if(mServerIdx == "2"){
            TextView cptime = (TextView) findViewById(R.id.rc32);
            cptime.setText("352 ms");
        }

    }

}
