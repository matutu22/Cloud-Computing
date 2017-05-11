
/**
 * Created by HOU ZHENQIAN on 26/04/2017.
 * Cluster and cloud computing
 * @unimelb
 * ID 720261
 */

import java.io.*;
import java.lang.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.security.*;
import java.security.cert.CertificateException;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;

import javax.net.ssl.*;

public class getASX200 {

    static final String SERVER_KEY_STORE_PASSWORD = "123456";
    static final String SERVER_TRUST_KEY_STORE_PASSWORD = "123456";
    static int port = 8008;
    static String adds = "localhost";

    static int perport = 8888;
    static String peradds = "localhost";
    public static BufferedReader reader;
    public static BufferedWriter writer;
    static boolean active = false;
    static boolean backup = true;
    static boolean lstbackup = false;
    static boolean state = false;

    public static void main (String[] args){
        System.out.println("ASX 200 HARVESTING SERVER IS RUNNING");
        System.out.println("------------------------------------");

        // get command information
        CmdLineArgs cmd = new CmdLineArgs();
        CmdLineParser parser = new CmdLineParser(cmd);
        try {
            parser.parseArgument(args);
            port = cmd.getCAServerPort();
            adds = cmd.getCAServerAdds();
            peradds = cmd.getCAServerpAdds();
            perport = cmd.getCAServerpPort();
        } catch (CmdLineException var4) {
            System.err.println(var4.getMessage());
            parser.printUsage(System.err);
        }


        //initial SSL connection
        ServerSocket listeningSocket = null;
        try {
            SSLContext ctx = SSLContext.getInstance("SSL");
            KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
            TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
            KeyStore ks = KeyStore.getInstance("JKS");
            KeyStore tks = KeyStore.getInstance("JKS");

            ks.load(new FileInputStream(System.getProperty("user.dir")+"/KeyStore/kserver.keystore"), SERVER_KEY_STORE_PASSWORD.toCharArray());
            tks.load(new FileInputStream(System.getProperty("user.dir")+"/KeyStore/tserver.keystore"), SERVER_TRUST_KEY_STORE_PASSWORD.toCharArray());
            kmf.init(ks, SERVER_KEY_STORE_PASSWORD.toCharArray());
            tmf.init(tks);
            ctx.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);
            listeningSocket = (SSLServerSocket) ctx.getServerSocketFactory().createServerSocket(port);


        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (KeyStoreException e) {
            e.printStackTrace();
        } catch (CertificateException e) {
            e.printStackTrace();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (UnrecoverableKeyException e) {
            e.printStackTrace();
        } catch (KeyManagementException e) {
            e.printStackTrace();
        }



        // continully listening
        while (true) {

            Socket clientSocket = null;
            try {
                clientSocket = listeningSocket.accept();
            } catch (IOException e) {
                e.printStackTrace();
            }

            try {
                reader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream(), "UTF-8"));
                writer = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream(), "UTF-8"));
            } catch (IOException e) {
                e.printStackTrace();
            }

            // reading message [time];[state]
            String temp = "";
            try {
                temp = reader.readLine();
              //  System.out.println(temp+"<<<<<<<<<<<<<<<<<<<<");
            } catch (IOException e) {
                System.out.println("[CHECKING] Received Starter Signal!");
                try {
                    clientSocket.close();
                } catch (IOException e1) {
                    e1.printStackTrace();
                }
            }


          /*  try {
                retime = receivetime.parse(read[0]);
            } catch (ParseException e) {
                e.printStackTrace();
            }
*/
            // checking state
            if ((temp.equals("STANDBY"))) {
                if (!lstbackup){
                    backup = true;
                    if ((!lstbackup)&&(backup!=lstbackup)) {
                        System.out.println("[CHECKING] Backup Server Standby!");
                        lstbackup =true;
                    }
                if (!lstbackup&&(backup!=lstbackup)) {
                    System.out.println("[CHECKING] Backup Server Recover!");
                    lstbackup =true;
                }
            } /*else {
                    //message is not update = more than 2 sec no [standby] message
                    System.out.println("[ ALARM* ] Backup Server Lost!");
                    backup = false;
                    lstbackup = false;
                }*/
            }else if (temp.equals("ACTIVE")){
                if (!active) {
                    active = true;
                    System.out.println("[CHECKING] Main Server is Active!");
                    System.out.println("[  SET   ] Standby!");
                }
                 /*else {
                    // message is not update = more than 2 sec no [active] message
                    // Active self
                    executive tusk = new executive("");
                    tusk.start();
                    state =true;
                    System.out.println("[ ALARM* ] Main Server Lost, Backup Server Is Active!");
                    System.out.println("[  SET   ] Active!");
                }*/
            } else if (temp.equals("HELLOW")){
                executive tusk = new executive("");
                tusk.start();
                state =true;
                System.out.println("[CHECKING] NO Active Server In System! ");
                System.out.println("[  SET   ] Active!");
            }

            if(state){
                Connection commu = new Connection(state,peradds,perport);
                commu.start();

            }else {
                Connection commu = new Connection(state,peradds,perport);
                commu.start();
            }

        }

    }
}