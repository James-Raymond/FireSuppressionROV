package com.example.james.servotesting;

import android.app.Activity;
import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.*;
import android.widget.SeekBar;


import java.io.*;
import java.net.Socket;

public class MainActivity extends Activity {


    EditText ipText;
    EditText portText;
    Button button;
    int progressBar;
    private Socket socket=null;
    private String ipaddress;
    private String port;
    public PrintWriter pw;




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ipText = (EditText) findViewById(R.id.ipText);
        portText = (EditText) findViewById(R.id.portText);
        final TextView text2 =(TextView) findViewById(R.id.seekBarText);
        button = (Button) findViewById(R.id.button);
        final SeekBar left = (SeekBar) findViewById(R.id.seekBar1);


        button.setOnClickListener(new View.OnClickListener() {

            private ProgressDialog pd = null;

            @Override
            public void onClick(View v) {
               ipaddress=ipText.getText().toString();
                port=portText.getText().toString();



            }
        });
        left.setOnSeekBarChangeListener(new SeekBar .OnSeekBarChangeListener() {


            @Override
            public void onProgressChanged(SeekBar seekBar1, int progress,
                                          boolean fromUser) {
                // TODO Auto-generated method stub
                text2.setText(String.valueOf(progress));
                progressBar = progress+2;
                try {
                    new AsyncAction().execute();
                }
                catch (Exception e){
                    e.printStackTrace();
                }


            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

                // TODO Auto-generated method stub
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }
        });

    }
    private class AsyncAction extends AsyncTask<String,Void,String>{


        @Override
        protected String doInBackground(String... params) {
            try {
                socket = new Socket(ipaddress, Integer.parseInt(port));
            } catch (IOException e) {
                e.printStackTrace();
            }

            PrintWriter outToServer = null;
            try {
                outToServer = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
            } catch (IOException e) {
                e.printStackTrace();
            }
            outToServer.print(progressBar);
            outToServer.flush();
            return null;
        }
    }
}


