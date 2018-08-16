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

public class BOC_Crawl {
	private Map<String, String[]> map = new HashMap<String, String[]>();
	private int counter = 0;

	public Document getHTMLDoc(String url) throws IOException {
		// 创建连接
		Connection connect = Jsoup.connect(url);
		Map<String, String> header = new HashMap<String, String>();
		header.put("Accept-Encoding", "gzip, deflate");
		header.put("Host", "www.boc.cn");
		header.put("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0");
		header.put("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8");
		header.put("Accept-Language", "en-US,en;q=0.5");
		header.put("Connection", "keep-alive");
		header.put("Referer", "http://www.boc.cn/custserv/bi2/");
		header.put("Upgrade-Insecure-Requests", "1");
		header.put("If-Modified-Since", "Mon, 13 Aug 2018 01:13:15 GMT");
		header.put("If-None-Match", "\"80479fcfa232d41:0\"");
		header.put("Cache-Control", "max-age=0");
		// 获取 response...不用配置请求头就行，，，配置请求头反而拿不到
		Document doc = connect.get();
		return doc;
	}

	public void HTMLExtract(Document doc) throws IOException, InterruptedException {
		// html解析
		Elements e = doc.getElementsByTag("tr");
		String[] array = e.toString().split("<tr>");
		// System.out.println(array[1]);
		// 产品代码：0，产品名称：1，期限：2，预期年化收益率：3，起售金额：4
		for (int i = 2; i < array.length; i++) {
			String[] content = new String[5];
			String[] array2 = array[i].split("</td>");
			if (array2.length > 4) {
				String product_name = array2[1].replaceAll("<td>", "").trim();
				String product_code = array2[0].replaceAll("<td>", "").trim();
				String expectRate = array2[3].replaceAll("<td>", "").replaceAll("<br>", "").trim();
				String startAmount = array2[4].replaceAll("<td>", "").trim();
				String duration = array2[2].replaceAll("<td>", "").trim();
				content[0] = product_name;
				content[1] = product_code;
				content[2] = expectRate;
				content[3] = startAmount;
				content[4] = duration;
				map.put(String.valueOf(counter++), content);
			}
		}

	}

	public static void main(String[] args) throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		BOC_Crawl crawl = new BOC_Crawl();
		String url = "http://www.boc.cn/fimarkets/cs8/201109/t20110922_1532694.html";
		crawl.HTMLExtract(crawl.getHTMLDoc(url));

		CsvWriter csvWriter = new CsvWriter("BOC_Product.csv", ',', Charset.forName("GBK"));
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
