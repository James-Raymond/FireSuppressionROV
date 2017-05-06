package com.example.james.servotesting;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.drawable.Drawable;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.view.KeyEvent;
import android.view.View;
import android.widget.*;

import java.io.*;
import java.net.Socket;

/**
 * Created by James on 01/05/2017.
 */


public class thermalActivity extends Activity {

    private Runnable r;
    private Handler handler;
    private Socket socket = null;
    private String ipaddress = "192.168.43.136";
    private String port = "8002";
    public String progressBar;
    private boolean threadRun= true;




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.thermal);

        final TextView text2 = (TextView) findViewById(R.id.seekBarText);
        final TextView textTilt = (TextView) findViewById(R.id.textView);
        final TextView textSpeed = (TextView) findViewById(R.id.textView2);

        final Button button = (Button) findViewById(R.id.button);
        final SeekBar pan = (SeekBar) findViewById(R.id.seekBar1);
        final SeekBar tilt = (SeekBar) findViewById(R.id.seekBar);
        final SeekBar speed = (SeekBar) findViewById(R.id.speed);
        final SeekBar turn = (SeekBar) findViewById(R.id.turn);
        final ImageView image = (ImageView) findViewById(R.id.imageView);

        thermalThread t = new thermalThread();

        button.setOnClickListener(new View.OnClickListener() {

            private ProgressDialog pd = null;

            @Override
            public void onClick(View v) {

                startActivity(new Intent(thermalActivity.this, MainActivity.class));
                thermalThread.yield();


            }
        });



        pan.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {


            @Override
            public void onProgressChanged(SeekBar seekBar1, int progress, boolean fromUser) {
                // TODO Auto-generated method stub
                text2.setText("P" + String.valueOf(progress + 1));
                //progress = progress;
                progressBar = "P" + progress;


            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar1) {
                try {
                    new thermalActivity.AsyncActionNew().execute();
                } catch (Exception e) {
                    e.printStackTrace();
                }

            }


        });

        tilt.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                textTilt.setText("T" + String.valueOf(progress));
                progress = progress;

                progressBar = "T" + progress;

            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                try {
                    new thermalActivity.AsyncActionNew().execute();
                } catch (Exception e) {
                    e.printStackTrace();
                }

            }
        });
        speed.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar speed, int progress, boolean fromUser) {
                textSpeed.setText("M" + String.valueOf(progress));
                progress = progress;

                progressBar = "M" + progress;


            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar speed) {
                try {
                    new thermalActivity.AsyncActionNew().execute();
                } catch (Exception e) {
                    e.printStackTrace();
                }

            }
        });


        turn.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar turn, int progress, boolean fromUser) {
                progressBar = "A" + progress;


            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar turn) {
                try {
                    new thermalActivity.AsyncActionNew().execute();
                } catch (Exception e) {
                    e.printStackTrace();
                }

            }
        });
        t.start();

        handler=new Handler();
         r=new Runnable() {
            public void run() {

                image.setImageDrawable(Drawable.createFromPath("/data/data/com.example.james.servotesting/thermalimage/newthermal.jpg"));
                //what ever you do here will be done after 3 seconds delay.
            }
        };


    }

    class thermalThread extends Thread {

        public void run() {
            while (threadRun==true) {

                try {


                    Socket socket = new Socket("192.168.43.136", 8000);
                    File newFolder = new File("/data/data/com.example.james.servotesting/thermalimage");
                    if (!newFolder.exists()) {
                        newFolder.mkdir();
                    }
                    File inputFile = new File(newFolder, "newthermal.jpg");

                    InputStream data = new BufferedInputStream(socket.getInputStream(), 9216);
                    byte[] pic = new byte[1024];
                    int total = 0;
                    int count = 0;
                    OutputStream ops = new FileOutputStream(inputFile);

                    while ((count = data.read(pic)) != -1) {
                        total += count;
                        System.out.println(count);
                        ops.write(pic, 0, count);
                        System.out.println("Image read");

                    }

                    data.close();
                    ops.close();



                    socket.close();

                } catch (IOException e) {
                    e.printStackTrace();
                }
                try {
                    thermalThread.sleep(20);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                System.out.println("Updating image");
               // handler.post(r);
                handler.post(r);

            }

           }

        }



    private class AsyncActionNew extends AsyncTask<String, Void, String> {

        private AsyncActionNew() throws IOException {
        }



        @Override
        protected String doInBackground(String... params) {
            try {
                System.out.println("connecting");
                System.out.println("Progress=" + getProgress());

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




}



