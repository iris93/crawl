import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
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

public class ICBC_Crawl {
	//计数器
	private int counter=0;
	//存储爬取结果Map<产品编码，Map<产品编码，名称，年收益率，起购金额，购买期限>>
	private Map<String, Map<String, String>> result = new HashMap<String, Map<String, String>>();
	public Document getHTMLDoc(String url) throws IOException {
		System.out.println(url);
		// 导入SSL证书
		System.setProperty("javax.net.ssl.trustStore", "/Users/liutong/Desktop/mybankicbccomcn.jks");
		// 创建连接
		Connection connect = Jsoup.connect(url);
		// Connection
		// connect=Jsoup.connect("https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession?dse_operationName=per_FinanceCurProListP3NSOp&p3bank_error_backid=120103&pageFlag=0&Area_code=4000&requestChannel=302");
		// Connection
		// connect=Jsoup.connect("https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession/dse_operationName=per_FinanceCurProListP3NSOp&useFinanceSolrFlag=1&orderclick=0&menuLabel=11|ALL&pageFlag_turn=2&nowPageNum_turn=2&Area_code=4000");
		// 构造请求头
		Map<String, String> header = new HashMap<String, String>();
		header.put("Accept-Encoding", "gzip, deflate, br");
		header.put("Host", "mybank.icbc.com.cn");
		header.put("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0");
		header.put("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8");
		header.put("Accept-Language", "en-US,en;q=0.5");
		header.put("Connection", "keep-alive");
		header.put("Cookie",
				"first_tip=0; guide_nologon=Tue, 06 Aug 2019 07:59:49 GMT; BIGipServerMyBank_IaaS_80_POOL=889557258.20480.0000; isP3bank=1; isEn_US=0; isPri=; firstZoneNo=%E6%B7%B1%E5%9C%B3_4000");
		header.put("Content-Type", "application/x-www-form-urlencoded");
		header.put("Referer", "https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession?dse_operationName=per_FinanceCurProListP3NSOp&p3bank_error_backid=120103&pageFlag=0&Area_code=4000&requestChannel=302");
		header.put("Upgrade-Insecure-Requests", "1");
		// 获取 response
		Connection data = connect.headers(header);
		Document doc = data.post();
		return doc;
	}

	public void HTMLExtract(Document doc) {
		// html解析
		for (int i = 0; i < 10; i++) {
			counter++;
			Map<String, String> record = new HashMap<String, String>();
			String myId = "circularcontainer_" + i;
			Element value_1 = doc.getElementById(myId);
			if(value_1!=null) {
				Elements value_2 = value_1.getElementsByClass("ebdp-pc4promote-circularcontainer-head-left");
				String str1 = value_2.toString();
				// 解析出产品名称和产品代码
				String[] array = str1.split("'");
				// 产品代码
				String productCode = array[1];
				// 产品名称
				String productName = array[3];
				//System.out.println("产品代码：" + productCode);
				//System.out.println("产品名称：" + productName);
				record.put("productCode", productCode);
				System.out.println(productCode);
				record.put("productName", productName);
				for (int j = 1; j <= 3; j++) {
					String str2 = "doublelabel" + j + "_" + i + "-content";
					Element value_3 = value_1.getElementById(str2);
					// System.out.println(value_3);
					if (j == 1) {
						String str3 = value_3.toString();
						String[] array2 = str3.split(">");
						String[] array3 = array2[1].split("<");
						String rate = array3[0].trim();
						// double rate=Double.parseDouble(array3[0].trim())/100;
						//System.out.println("年化收益率：" + rate);
						record.put("annuralRate", rate);
					}
					if (j == 2) {
						Elements value_4 = value_3.getElementsByTag("b");
						String str4 = value_4.toString();
						String[] array2 = str4.split(">");
						String[] array3 = array2[1].split("<");
						String startAmount = array3[0].trim();
						// double startAmount=Double.parseDouble(array3[0].trim());
						//System.out.println("起购金额：" + startAmount + " 万");
						record.put("startAmount", startAmount);
					}
					if (j == 3) {
						String str5 = value_3.toString();
						String duration="";
						if (str5.contains("无固定期限")) {
							duration="无固定期限";
							//System.out.println("期限：无固定期限");
						} else {
							Elements value_4 = value_3.getElementsByTag("b");
							String str4 = value_4.toString();
							String[] array2 = str4.split(">");
							String[] array3 = array2[1].split("<");
							String date = array3[0].trim();
							// int startAmount=Integer.parseInt(array3[0].trim());
							//System.out.println("期限：" + date + " 天");
							duration=date;
						}
						record.put("duration", duration);
					}
				}
				result.put(productCode, record);
			}
			}
			
	}

	public static void main(String[] args) throws IOException {
		ICBC_Crawl crawl=new ICBC_Crawl();
		Map<String, Map<String, String>> totalResult=new HashMap<String, Map<String, String>>(); 
		// 通过控制变量nowPageNum_turn：1-17来获取17页理财产品信息
		for (int pageNum = 1; pageNum <= 17; pageNum++) {
			String url="https://mybank.icbc.com.cn/servlet/ICBCBaseReqServletNoSession?dse_operationName=per_FinanceCurProListP3NSOp&useFinanceSolrFlag=1&orderclick=0&menuLabel=11|ALL&pageFlag_turn=2&Area_code=4000&nowPageNum_turn="+pageNum;
            Document doc=crawl.getHTMLDoc(url);   
            crawl.HTMLExtract(doc);
		}
		System.out.println(crawl.counter);
		//遍历result,取出结果写进文件
		CsvWriter csvWriter = new CsvWriter("ICBC_Product.csv",',', Charset.forName("GBK"));
		// 写表头
        String[] headers = {"产品名称","产品代码","预期年化收益率/业绩基准","起购金额","期限"};
       // String[] content = {"12365","张山","34"};
        csvWriter.writeRecord(headers);
		Iterator iter=crawl.result.entrySet().iterator();
		while(iter.hasNext()) {
			Entry en=(Entry)iter.next();
			Map<String,String>m=(Map<String, String>) en.getValue();
			String[] content={m.get("productName"),m.get("productCode"),m.get("annuralRate"),m.get("startAmount"),m.get("duration")};
		    csvWriter.writeRecord(content);
		}
        csvWriter.flush();
        csvWriter.close();
	}

}
