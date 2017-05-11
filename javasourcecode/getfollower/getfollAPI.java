import java.io.IOException;

/**
 * Created by HOU ZHENQIAN on 1/05/2017.
 */
public class getfollAPI {

    public static void main(String[] args) {
        long [] ID = new long[22];
        ID [0]  =  19050000;
        ID [1]  =  28002931;
        ID [2]  =  3099501;
        ID [3]  =  877404932;
        ID [4]  =  18700398;
        ID [5]  =  2768501;
        ID [6]  =  93969270;
        ID [7]  =  56773228;
        ID [8]  =  21814628;
        ID [9]  =  307749870;
        ID [10] =  90360929;
        ID [11] =  2576461;
        ID [12] =  14862794;
        ID [13] =  436226316;
        ID [14] =  39206861;
        ID [15] =  890102851;
        ID [16] =  46054208;
        ID [17] =  41312733;
        ID [18] =  20104025;
        ID [19] =  23546978;
        ID [20] =  28722856;
        ID [21] =  29406687;


        for (int i= 0;i<=0;i++ ){
            System.out.println("Thread "+ i + " Standby !    "+"ID: "+ID[i]);
            CollectTwitters tusk = null;
            try {
                tusk = new CollectTwitters(ID [i], args);
            } catch (IOException e) {
                e.printStackTrace();
            }
            tusk.start();
        }

    }

}
