package com.example.james.servotesting;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.*;
import java.io.*;
import java.net.Socket;

public class MainActivity extends Activity {

    private Socket socket=null;
    private String ipaddress = "192.168.43.136";
    private String port = "8002" ;
    public String progressBar;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final TextView text2 =(TextView) findViewById(R.id.seekBarText);
        final TextView textTilt =(TextView) findViewById(R.id.textView);
        final TextView textSpeed =(TextView) findViewById(R.id.textView2);

        final Button button = (Button) findViewById(R.id.button);
        final SeekBar pan = (SeekBar) findViewById(R.id.seekBar1);
        final SeekBar tilt = (SeekBar) findViewById(R.id.seekBar);
        final SeekBar speed = (SeekBar) findViewById(R.id.speed);
        final SeekBar turn = (SeekBar) findViewById(R.id.turn);

        final VideoView video = (VideoView) findViewById(R.id.videoView);

        MediaController mediaCon = new MediaController(this);
        video.setMediaController((mediaCon));

        System.out.println("Trying to connect");


        video.setVideoURI(Uri.parse("http://192.168.43.136:8160/"));
        video.start();

        button.setOnClickListener(new View.OnClickListener() {

            private ProgressDialog pd = null;

            @Override
            public void onClick(View v) {

                startActivity(new Intent(MainActivity.this, thermalActivity.class));


            }
        });

        pan.setOnSeekBarChangeListener(new SeekBar .OnSeekBarChangeListener() {


            @Override
            public void onProgressChanged(SeekBar seekBar1, int progress, boolean fromUser) {
                // TODO Auto-generated method stub
                text2.setText("P"+String.valueOf(progress+1));
                //progress = progress;
                progressBar = "P"+progress;



            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar1) {
                try {
                    new AsyncAction().execute();
                }
                catch (Exception e){
                    e.printStackTrace();
                }

            }


        });

        tilt.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                textTilt.setText("T"+String.valueOf(progress));
                progress = progress;

                progressBar = "T"+progress;

            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                try {
                    new AsyncAction().execute();
                }
                catch (Exception e){
                    e.printStackTrace();
                }

            }
        });
        speed.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar speed, int progress, boolean fromUser) {
                textSpeed.setText("M"+String.valueOf(progress));
                progress = progress;

                progressBar = "M"+progress;


            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar speed) {
                try {
                    new AsyncAction().execute();
                }
                catch (Exception e){
                    e.printStackTrace();
                }

            }
        });


        turn.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar turn, int progress, boolean fromUser) {
                progressBar = "A"+progress;


            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar turn) {
                try {
                    new AsyncAction().execute();
                }
                catch (Exception e){
                    e.printStackTrace();
                }

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

        public String getProgress() {
            System.out.println(progressBar);

            return progressBar;
        }
    }
    @Override
    protected void onDestroy() {
        super.onDestroy();
        // close all your threads
    }

}


