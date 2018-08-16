import java.io.IOException;
import java.nio.charset.Charset;
import java.util.ArrayList;
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

public class CMBC_Crawl {
	private Map<String, String[]> map = new HashMap<String, String[]>();
	private int counter = 0;
	java.util.Random r=new java.util.Random();

	public Document getHTMLDoc(String url, String pageNum) throws IOException {
		// 创建连接
		Connection connect = Jsoup.connect(url);
		Map<String, String> header = new HashMap<String, String>();
		header.put("Accept-Encoding", "gzip, deflate");
		header.put("Host", "www.cmbc.com.cn");
		header.put("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0");
		header.put("Accept", "text/plain, */*; q=0.01");
		header.put("Accept-Language", "en-US,en;q=0.5");
		header.put("Connection", "keep-alive");
		header.put("Cache-Control", "max-age=0");
		header.put("Cookie",
				"JSESSIONID=t6Mw9aLqsdY0LLgzzhKDDZTIajXjL3NE-bwkzfpXUPkgVcSmCe0T!-1623711326; BIGipServerCMBCWEB_menhuwangzhan_8000_web_pool=2236809226.2336.0000");
		header.put("Referer", "http://www.cmbc.com.cn/channelApp/finance/financial.jsp");
		header.put("X-Requested-With", "XMLHttpRequest");
		header.put("Content-Type", "application/json;charset=UTF-8");
		String jsonStr = "{\"request\":{\"body\":{\"page\":" + pageNum
				+ ",\"row\":10},\"header\":{\"device\":{\"model\":\"SM-N7508V\",\"osVersion\":\"4.3\",\"imei\":\"352203064891579\",\"isRoot\":\"1\",\"nfc\":\"1\",\"brand\":\"samsung\",\"mac\":\"B8:5A:73:94:8F:E6\",\"uuid\":\"45cnqzgwplsduran7ib8fw3aa\",\"osType\":\"01\"},\"appId\":\"1\",\"net\":{\"ssid\":\"oa-wlan\",\"netType\":\"WIFI_oa-wlan\",\"cid\":\"17129544\",\"lac\":\"41043\",\"isp\":\"\",\"ip\":\"195.214.145.199\"},\"appVersion\":\"3.60\",\"transId\":\"Financialpage\",\"reqSeq\":\"0\"}}}";
		// 获取 response
		Document doc = connect.requestBody(jsonStr).ignoreContentType(true).headers(header).ignoreHttpErrors(true)
				.post();// 这个很重要
		/*
		 * Elements e=doc.getElementsByTag("body"); System.out.println(e.toString());
		 */
		return doc;
	}

	public Document getSubHTMLDoc(String url,String code) throws IOException {
		// 创建连接
		Connection connect = Jsoup.connect(url);
		Map<String, String> header = new HashMap<String, String>();
		header.put("Accept-Encoding", "gzip, deflate");
		header.put("Host", "www.cmbc.com.cn");
		header.put("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0");
		header.put("Accept", "text/plain, */*; q=0.01");
		header.put("Accept-Language", "en-US,en;q=0.5");
		header.put("Connection", "keep-alive");
		header.put("Cache-Control", "max-age=0");
		header.put("Cookie",
				"JSESSIONID=t6Mw9aLqsdY0LLgzzhKDDZTIajXjL3NE-bwkzfpXUPkgVcSmCe0T!-1623711326; BIGipServerCMBCWEB_menhuwangzhan_8000_web_pool=2236809226.2336.0000");
		header.put("Referer", "http://www.cmbc.com.cn/channelApp/finance/financialDetail.jsp?prd_code=FSAB130206");
		header.put("X-Requested-With", "XMLHttpRequest");
		header.put("Content-Type", "application/json;charset=UTF-8");
		String jsonStr = "{\"request\":{\"body\":{\"prd_code\":\""+code+"\"},\"header\":{\"device\":{\"model\":\"SM-N7508V\",\"osVersion\":\"4.3\",\"imei\":\"352203064891579\",\"isRoot\":\"1\",\"nfc\":\"1\",\"brand\":\"samsung\",\"mac\":\"B8:5A:73:94:8F:E6\",\"uuid\":\"45cnqzgwplsduran7ib8fw3aa\",\"osType\":\"01\"},\"appId\":\"1\",\"net\":{\"ssid\":\"oa-wlan\",\"netType\":\"WIFI_oa-wlan\",\"cid\":\"17129544\",\"lac\":\"41043\",\"isp\":\"\",\"ip\":\"195.214.145.199\"},\"appVersion\":\"3.60\",\"transId\":\"FinancialDetail\",\"reqSeq\":\"0\"}}}";
		// 获取 response
		Document doc = connect.requestBody(jsonStr).ignoreContentType(true).headers(header).ignoreHttpErrors(true)
				.post();
		//System.out.println(doc.toString());
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
		JSONObject json_2 = (JSONObject) json.get("returnData");
		JSONArray ja = json_2.getJSONArray("list");
		// System.out.println(json_2.getJSONArray("list"));
		for (Object s : ja) {
			String[] content = new String[5];
			JSONObject jp = (JSONObject) s;
			// 产品名称
			String product_name = jp.get("PRD_NAME").toString();
			// 产品代码
			String product_code = jp.get("PRD_CODE").toString();
			// 产品期限
			String duration = jp.get("LIVE_TIME").toString();
			// 起售金额
			String startAmount = jp.get("PFIRST_AMT").toString();
			// 预期收益率
			String expectRate = jp.get("NEXT_INCOME_RATE").toString();
			if(expectRate.equals("0.00%")){
				// 如果收益率为0.00%，则需要进一步去产品详情页面查看收益率，确定最终收益率是否为0
				String sub_url = "http://www.cmbc.com.cn/channelApp/ajax/FinancialDetail";
				Document document = getSubHTMLDoc(sub_url,product_code);
				// html解析
				Elements e2 = document.getElementsByTag("body");
				String[] array3 = e2.toString().split(">");
				String[] array4 = array3[1].split("<");
				String jsonStr2 = array4[0];
				// 解析JSON
				JSONObject json2 = JSONObject.fromObject(jsonStr2);
				JSONObject json_3 = (JSONObject) json2.get("returnData");
				//System.out.println(json_3.toString());
				//Thread.sleep(1000+r.nextInt(2)*1000);
				if (json_3.get("Income_Rate") != null) {
					String str=json_3.get("Income_Rate").toString();
					if(!str.equals("5.15%")) {
						//"Next_Income_Rate"的默认值是5.15%而非0.00%
						expectRate = str;
					}
				}
			}
			content[0] = product_name;
			content[1] = product_code;
			content[2] = expectRate;
			content[3] = startAmount;
			content[4] = duration;
			//System.out.println(product_name+" "+expectRate);
			for(String st:content) {
				System.out.print(st+" ");
			}
			System.out.println("");
			map.put(String.valueOf(counter++), content);
		}
	}

	public static void main(String[] args) throws IOException, InterruptedException {
		// TODO Auto-generated method stub
		CMBC_Crawl crawl = new CMBC_Crawl();
		String url = "http://www.cmbc.com.cn/channelApp/ajax/Financialpage";
		for (int i = 1; i <= 61; i++) {
			Thread.sleep(2000);
			System.out.println(i);
			if(i%3==0) {
				Thread.sleep(4000);
			}
			crawl.HTMLExtract(crawl.getHTMLDoc(url, String.valueOf(i)));
		}
		// 结果输出
		CsvWriter csvWriter = new CsvWriter("CMBC_Product.csv", ',', Charset.forName("GBK"));
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
