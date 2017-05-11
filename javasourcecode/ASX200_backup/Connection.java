import javax.net.ssl.*;
import java.io.*;
import java.net.Socket;
import java.security.*;
import java.lang.*;
import java.security.cert.CertificateException;

/**
 * Created by HOU ZHENQIAN on 27/04/2017.
 */
public class Connection extends Thread{

    boolean state;
    static int perport = 8888;
    static String peradds = "localhost";
    public static BufferedWriter writer;
    static final String SERVER_KEY_STORE_PASSWORD = "123456";
    static final String SERVER_TRUST_KEY_STORE_PASSWORD = "123456";

    public Connection(boolean state,String peradds, int perport) {

        this.state = state;
        this.peradds = peradds;
        this.perport = perport;
    }


    @Override
    public void run(){

        SSLContext ctx = null;
        try {
            ctx = SSLContext.getInstance("SSL");
            KeyManagerFactory  kmf = KeyManagerFactory.getInstance("SunX509");
            TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
            KeyStore  ks = KeyStore.getInstance("JKS");
            KeyStore  tks = KeyStore.getInstance("JKS");
            ks.load(new FileInputStream(System.getProperty("user.dir")+"/KeyStore/kclient.keystore"), SERVER_KEY_STORE_PASSWORD.toCharArray());
            tks.load(new FileInputStream(System.getProperty("user.dir")+"/KeyStore/tclient.keystore"), SERVER_TRUST_KEY_STORE_PASSWORD.toCharArray());
            kmf.init(ks, SERVER_KEY_STORE_PASSWORD.toCharArray());
            tmf.init(tks);
            ctx.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

        } catch (KeyStoreException e) {
            e.printStackTrace();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (CertificateException e) {
            e.printStackTrace();
        } catch (UnrecoverableKeyException e) {
            e.printStackTrace();
        } catch (KeyManagementException e) {
            e.printStackTrace();
        }

            Socket coopsocket = null;
            BufferedWriter cooperation = null;
            try {
                coopsocket = (SSLSocket) ctx.getSocketFactory().createSocket(peradds, perport);
                cooperation = new BufferedWriter(new OutputStreamWriter(coopsocket.getOutputStream(), "UTF-8"));
            } catch (IOException e) {
                System.out.println("[ ALARM  ] Heartbeat Signal Lost!");
                Thread.interrupted();
            }

            try {
            if (state) {
              //  System.out.println("[SENDING ] Sending Active Signal To Backup Server!");
                    cooperation.write("ACTIVE");
                    cooperation.flush();
                    cooperation.close();
            }else {
               // System.out.println("[SENDING ] Sending Backup Signal To Main Server!");
                    cooperation.write("STANDBY");
                    cooperation.flush();
                    cooperation.close();
            }
            } catch (IOException e) {
                System.out.println("[ ALARM  ] Heartbeat Signal Lost!");
                Thread.interrupted();
                Thread.interrupted();
                if (state){
                    System.out.println("[ ALARM  ] Backup Server Lost!");
                }else {
                    System.out.println("[ ALARM  ] Main Server Lost!");
                    System.out.println("[  SET   ] Active");
                    executive tusk = new executive("");
                    tusk.start();
                    state = true;
                }
            }

            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

    }
}
