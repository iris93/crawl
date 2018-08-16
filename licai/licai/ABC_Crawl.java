import java.io.IOException;
import java.nio.charset.Charset;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;

import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import com.csvreader.CsvWriter;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

public class ABC_Crawl {
	private Map<String, String[]> map = new HashMap<String, String[]>();
	private int counter = 0;

	public Document getHTMLDoc(String url) throws IOException {
		// 创建连接
		Connection connect = Jsoup.connect(url);
		Map<String, String> header = new HashMap<String, String>();
		header.put("Accept-Encoding", "gzip, deflate");
		header.put("Host", "ewealth.abchina.com");
		header.put("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0");
		header.put("Accept", "application/json, text/javascript, */*; q=0.01");
		header.put("Accept-Language", "en-US,en;q=0.5");
		header.put("Connection", "keep-alive");
		header.put("Cache-Control", "max-age=0");
		header.put("Cookie",
				" BIGipServerpool_pt_ewealth=3797543690.47752.0000; WT_FPC=id=10.235.177.249-2473792032.30683858:lv=1534146067206:ss=1534145880810; BIGipServerpool_pt_ewealth_app=3814320906.48008.0000; bdata=%5B%7B%22Name%22%3A%22%E2%80%9C%E9%87%91%E9%92%A5%E5%8C%99%C2%B7%E5%A6%82%E6%84%8F%E7%BB%84%E5%90%88%C2%B790%E5%A4%A9%E2%80%9D%E6%B2%AA%E6%B7%B1300%E6%8C%87%E6%95%B0%E5%88%B0%E6%9C%9F%E7%AA%84%E5%B9%85%E6%B3%A2%E5%8A%A8%E4%BA%BA%E6%B0%91%E5%B8%81%E7%90%86%E8%B4%A2%E4%BA%A7%E5%93%81%22%2C%22Url%22%3A%22%2Ffs%2FADRY176090B.htm%22%2C%22Rate%22%3A%223%25-5%25%22%2C%22User%22%3A%22%22%7D%5D; UserTag=null");
		header.put("Referer",
				"http://ewealth.abchina.com/fs/filter/?saleSate=%E5%BD%93%E5%89%8D%E5%9C%A8%E5%94%AE&prodLimit=&prodYildType=");
		// header.put("Params",
		// "i=1;s=15;o=0;w=%25E5%258F%25AF%25E5%2594%25AE%257C%257C%257C%257C%257C%257C%257C1%257C%257C0%257C%257C0");
		// 获取 response
		Document doc = connect.ignoreContentType(true).headers(header).ignoreHttpErrors(true).get();
		return doc;
	}

	public void HTMLExtract(Document doc) throws IOException, InterruptedException {
		// html解析
		Elements e = doc.getElementsByTag("body");
		String[] array = e.toString().split(">");
		String[] array2 = array[1].split("<");
		String jsonStr = array2[0];
		// 解析JSON
		JSONObject json = JSONObject.fromObject(jsonStr);
		JSONObject json_2 = (JSONObject) json.get("Data");
		JSONArray ja = json_2.getJSONArray("Table");
		for (Object s : ja) {
			String[] content = new String[5];
			JSONObject jp = (JSONObject) s;
			// System.out.println(jp.toString());
			// 产品名称
			String product_name = jp.get("ProdName").toString();
			// 产品代码
			String product_code = jp.get("ProductNo").toString();
			// 产品期限
			String duration = jp.get("ProdLimit").toString();
			// 起售金额
			String startAmount = jp.get("PurStarAmo").toString();
			// 预期收益率
			String expectRate = jp.get("ProdProfit").toString();
			content[0] = product_name;
			content[1] = product_code;
			content[2] = expectRate;
			content[3] = startAmount;
			content[4] = duration;
			System.out.println(product_name+" "+expectRate);
			map.put(String.valueOf(counter++), content);
		}

	}

	public static void main(String[] args) throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		ABC_Crawl crawl = new ABC_Crawl();
		for(int i=1;i<=5;i++) {
			String url = "http://ewealth.abchina.com/app/data/api/DataService/BoeProductV2?i="+i+"&s=15&o=0&w=%25E5%258F%25AF%25E5%2594%25AE%257C%257C%257C%257C%257C%257C%257C1%257C%257C0%257C%257C0";
			crawl.HTMLExtract(crawl.getHTMLDoc(url));
		}
		CsvWriter csvWriter = new CsvWriter("ABC_Product.csv", ',', Charset.forName("GBK"));
		// 写表头
		String[] headers = { "产品名称", "产品代码", "预期年化收益率/业绩基准", "起购金额", "期限" };
		csvWriter.writeRecord(headers);
		Iterator iter = crawl.map.entrySet().iterator();
		while (iter.hasNext()) {
			Entry en = (Entry) iter.next();
			String[] content = (String[]) en.getValue();
			csvWriter.writeRecord(content);
		}
		csvWriter.flush();
		csvWriter.close();
	}


}
