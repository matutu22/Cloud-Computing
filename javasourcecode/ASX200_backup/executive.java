/**
 * Created by HOU ZHENQIAN on 26/04/2017.
 * Cluster and cloud computing
 * @unimelb
 * ID 720261
 */

import org.jsoup.Jsoup;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.net.MalformedURLException;
import java.util.Date;
import org.lightcouch.CouchDbClient;
import org.lightcouch.CouchDbException;
import org.lightcouch.CouchDbProperties;
import org.lightcouch.DocumentConflictException;
import org.json.simple.JSONObject;

public class executive extends Thread {
    private static CouchDbClient DbClient;
    String command;

    public executive(String command) {
        this.command = command;
    }

    @Override
    public void run(){
        String add = "https://www.google.com/finance?q=INDEXASX:XJO";
        Date now = new Date();
        String old = null;
        System.out.println("[ START  ] ASX200 Harvest Server Start At:"+now+"***");
        File file = new File(now.getDate()+"_"+(now.getMonth()+1)+" ASX200.txt");
        BufferedWriter bw =null;
        String ASX200 = null;
        FileWriter fw = null;
        try {
            fw = new FileWriter(file);
        } catch (IOException e) {
            e.printStackTrace();
        }
        bw = new BufferedWriter(fw);


        //inint DB
        CouchDbProperties ASX_200 = new CouchDbProperties()
                .setDbName("asx_200")
                .setCreateDbIfNotExist(true)
                .setProtocol("http")
                .setHost("localhost")
                .setPort(5984)
                .setUsername("admin")
                .setPassword("123");
        DbClient = new CouchDbClient(ASX_200);




        while (!command.equals("exit")) {
            now = new Date();
            int day = now.getDay();
            int hour = now.getHours();
            if (day <= 5 && (hour >= 10 && hour < 16)) {
                try {
                    org.jsoup.nodes.Document cont = Jsoup.connect(add).get();
                    String[] part = cont.toString().split("price\\\" content=\\\"");

                    if (part.length>1){
                        ASX200 = part[1].substring(0, 8);}

                    if (!ASX200.equals(old)) {
                        System.out.println("[ AXS200 ] "+now + "        ASX200: " + ASX200);
                        old=ASX200;
                        bw.write(now+";"+ ASX200+" "+"\n");
                        bw.flush();
                        JSONObject msg = new JSONObject();
                        msg.put("_id",now);
                        msg.put("value",ASX200);
                        try {
                            DbClient.save(msg);
                        }catch(DocumentConflictException doc){
                            System.out.println("document error");
                        }catch (CouchDbException e){
                            System.out.println("couch db error");
                        }
                    }
                    Thread.sleep(3000);
                } catch (MalformedURLException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

            } else{
                if(hour ==16){
                    System.out.println("*****   CLOSED!    Powered by Google Finance    *****");
                    try {
                        Thread.sleep(64200000);
                        now = new Date();
                        file = new File(now.getDate()+"_"+(now.getMonth()+1)+" ASX200.txt");
                        try {
                            fw = new FileWriter(file);
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                        bw = new BufferedWriter(fw);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }else {
                    try {
                        Thread.sleep(5000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }
}



