package com.example.ebias;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.annotation.TargetApi;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.StrictMode;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.text.TextUtils;
import android.view.KeyEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.inputmethod.EditorInfo;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.HttpGet;

import cz.msebera.android.httpclient.Header;
import cz.msebera.android.httpclient.HttpHost;
import cz.msebera.android.httpclient.HttpRequest;
import cz.msebera.android.httpclient.HttpResponse;
import cz.msebera.android.httpclient.client.ClientProtocolException;
import cz.msebera.android.httpclient.client.HttpClient;
import cz.msebera.android.httpclient.client.ResponseHandler;
import cz.msebera.android.httpclient.client.methods.HttpUriRequest;
import cz.msebera.android.httpclient.conn.ClientConnectionManager;
import cz.msebera.android.httpclient.impl.client.DefaultHttpClient;
import cz.msebera.android.httpclient.params.HttpParams;
import cz.msebera.android.httpclient.protocol.HttpContext;

import static android.Manifest.permission.READ_CONTACTS;

/**
 * A login screen that offers login via email/password.
 */
public class LoginActivity extends AppCompatActivity{

    /**
     * Id to identity READ_CONTACTS permission request.
     */

    private static final int REQUEST_READ_CONTACTS = 0;

    /**
     * A dummy authentication store containing known user names and passwords.
     * TODO: remove after connecting to a real authentication system.
     */
    private static final String[] DUMMY_CREDENTIALS = new String[]{
            "foo@example.com:hello", "bar@example.com:world"
    };

    // UI references.
    private String mUserID;
    private String mServer;
    private String mAlgo;
    private Integer mUserIndex;
    private Integer mServerIndex;
    private Integer mAlgoIndex;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        Button mEmailSignInButton = (Button) findViewById(R.id.email_sign_in_button);
        mEmailSignInButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    attemptLogin();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    private void attemptLogin() throws IOException {

        if (android.os.Build.VERSION.SDK_INT > 9)
        {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        Spinner user = (Spinner) findViewById(R.id.user);

        Spinner server = (Spinner) findViewById(R.id.server);
        Spinner algo = (Spinner) findViewById(R.id.algoSelect);
        mUserID = user.getSelectedItem().toString();
        mServer = server.getSelectedItem().toString();
        mAlgo = algo.getSelectedItem().toString();
        mUserIndex = user.getSelectedItemPosition();
        mServerIndex = server.getSelectedItemPosition();
        mAlgoIndex = algo.getSelectedItemPosition();
        Uri.Builder builder = new Uri.Builder();// = new URL("http://192.168.1.14:5050/hello.py?1&Bayes/");
        builder.scheme("http");
        switch (mServerIndex){
            case 0:
                break;
            case 1:

                builder.encodedAuthority("192.168.1.14:5050");// new URL("http:///hello.py?1/");
                break;
            case 2:
                builder.authority("3.14.184.137");
                break;
            default:
                builder.encodedAuthority("192.168.1.14:5050");
                break;
        }

        switch (mAlgoIndex){
            case 0:
                builder.appendPath("LRModel.py");
                break;
            case 1:
                builder.appendPath("NaiveBayes.py");
                break;
            case 2:
                builder.appendPath("KNN.py");
                break;
            case 3:
                builder.appendPath("Neural.py");
                break;
        }
        Integer userP = mUserIndex+1;
        String paramUser = userP.toString();
        builder.appendQueryParameter("user", paramUser);
        String uri = builder.build().toString();
//        uri = uri+"?'user'='"+userP+"'";
        uri = uri+"/";
//        System.out.print(uri);

        URL url = new URL(uri);
        BufferedReader in = new BufferedReader(
                new InputStreamReader(
                        url.openStream()));

        String inputLine;

        if((inputLine = in.readLine()) != null) {
//        if((inputLine) != null) {
            System.out.println("aa" + inputLine+"aa");
            System.out.println(inputLine.getClass());
//            String s = "Hello World";
//            if(inputLine.equals(s)){
            if(inputLine.equals("1")){
                in.close();
                Intent t = new Intent(LoginActivity.this, MainActivity.class);
                t.putExtra("user", mUserID);
                t.putExtra("algo", mAlgo);
                t.putExtra("server", mServer);
                t.putExtra("userIdx", mUserIndex);
                t.putExtra("algoIdx", mAlgoIndex);
                t.putExtra("serverIdx", mServerIndex);
                startActivity(t);
            }
            else{
                in.close();
                new AlertDialog.Builder(this).setTitle("Login Error").setMessage("The user could not be logged in. Please try again.")
                        .setPositiveButton(android.R.string.ok, null).show();
            }

        }

        in.close();

    }
}
