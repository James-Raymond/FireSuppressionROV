package com.example.james.servotesting;

import android.app.Activity;
import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.*;
import android.widget.SeekBar;
import android.widget.ProgressBar;


import java.io.*;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.Socket;

import static android.R.id.progress;


public class MainActivity extends Activity {


    EditText ipText;
    EditText portText;
    Button button;
    private Socket socket=null;
    private String ipaddress;
    private String port;
    public int progressBar;
    public boolean progressFlag = false;



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
                System.out.println("Trying to connect");

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
                progressBar = progress+3;
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

        private AsyncAction() throws IOException {
        }


        @Override
        protected String doInBackground(String... params) {
            try {
                System.out.println("Trying to connect");
                System.out.println("Progress="+getProgress());

                socket = new Socket(ipaddress, Integer.parseInt(port));
                PrintWriter outToServer = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
                System.out.println(getProgress());
                outToServer.print(getProgress());
                outToServer.flush();

            } catch (IOException e) {
                e.printStackTrace();
            }

            return null;
        }

        public int getProgress() {
            System.out.println(progressBar);

            return progressBar;
        }
    }



}


