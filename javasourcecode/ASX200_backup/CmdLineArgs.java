/**
 * Created by HOU ZHENQIAN on 26/04/2017.
 */

    import org.kohsuke.args4j.Option;

    public class CmdLineArgs {

        @Option(required = true, name = "-a", usage = "serveradd")
        private String adds;

        @Option(required = true, name = "-p", usage = "serverport")
        private int port;

        @Option(required = true, name = "-pa", usage = "serverpadds")
        private String padds;

        @Option(required = true, name = "-pp", usage = "serverpport")
        private int pPort;


        public String getCAServerAdds() {
            return adds;
        }

        public int getCAServerPort() {
            return port;
        }

        public int getCAServerpPort() {
            return pPort;
        }

        public String getCAServerpAdds() {
            return padds;
        }

    }

