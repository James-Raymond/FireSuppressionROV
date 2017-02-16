/*
James Raymond
Lab Exam Repeat 13/01/2017
Mobile Device Programming

Servlet

 */
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.UnavailableException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.*;

import static java.lang.Double.valueOf;


@WebServlet(name = "Servlet", urlPatterns = {"/data"})
public class Servlet extends HttpServlet {

    double totalPayments;

    String command;

    String temp;

    protected void doPost( HttpServletRequest request, HttpServletResponse response )throws ServletException, IOException {
        try {
            BufferedReader reader = request.getReader();
            StringBuilder sb = new StringBuilder();
            try {
                String line = "";
                line=reader.readLine();
                while(line != null) {
                    sb.append(line);
                    sb.append("\n");
                    line=reader.readLine();
                }
                System.out.println(sb.toString());

                if(sb.toString().contains("_")){
                    System.out.print(sb.toString());
                    String[] parts = sb.toString().split("_");// splits each word
                    command = parts[1];
                    System.out.println(command);
                    if( command == "2") {
                        System.out.println(" a revieved ");
                    }
                }
            }
            catch(Exception e)
            {
                e.printStackTrace();
            }
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }

    }


}
