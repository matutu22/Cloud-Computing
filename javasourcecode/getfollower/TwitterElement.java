import java.util.Date;
import com.google.gson.annotations.SerializedName;
import org.lightcouch.Document;
import twitter4j.*;
import java.util.Date;

/**
 * Created by HOU ZHENQIAN on 15/04/2017.
 * ID: 720261
 * UNIMELB
 */

public class TwitterElement {

    @SerializedName("_id")
    private String id;
    @SerializedName("_rev")
    private String revision;
    @SerializedName("geoLocation")
    private GeoLocation geoLocation;
    @SerializedName("createdAt")
    private Date createdAt;
    @SerializedName("place")
    private Place place;
    @SerializedName("lang")
    private String lang;
    @SerializedName("text")
    private String text;
    @SerializedName("isRetweet")
    private boolean isRetweet;
    @SerializedName("retweetedStatusText")
    private String retweetedStatusText;
    @SerializedName("source")
    private String source;

    public TwitterElement(Status status){
        id =  String.valueOf(status.getId());
        geoLocation = status.getGeoLocation();
        createdAt = status.getCreatedAt();
        place = status.getPlace();
        lang = status.getLang();
        text = status.getText();
        if (status.getRetweetedStatus() != null ){
            isRetweet = true;
            retweetedStatusText =  status.getRetweetedStatus().getText();
        } else {
            isRetweet = false;
        }
        source = status.getSource();
    }
}
