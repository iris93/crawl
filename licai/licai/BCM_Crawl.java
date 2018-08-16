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

public class BCM_Crawl {
	private Map<String,String[]>map=new HashMap<String,String[]>();
	private int counter=0;

	public Document getHTMLDoc(String url) throws IOException {
		// 创建连接
		Connection connect = Jsoup.connect(url);
		Map<String, String> header = new HashMap<String, String>();
		header.put("Accept-Encoding", "gzip, deflate");
		header.put("Host", "www.bankcomm.com");
		header.put("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0");
		header.put("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8");
		header.put("Accept-Language", "en-US,en;q=0.5");
		header.put("Connection", "keep-alive");
		header.put("Cache-Control", "max-age=0");
		header.put("Cookie","your_cookie_name=59.37.11.101.1533795779778746; JSESSIONID=00004WSrHCW2fU4evALQFIKB0M7:-1");
		header.put("Referer", "http://www.bankcomm.com/BankCommSite/jyjr/cn/lcpd/index.jsp?");
		header.put("Upgrade-Insecure-Requests", "1");
		//header.put("If-None-Match", "pv4919da6a088a64f83d67d37d1bf5fd06");
		// 获取 response
		Document doc = connect.ignoreContentType(true).headers(header).ignoreHttpErrors(true).timeout(3000).get() ;
		return doc;
	}
	public void HTMLExtract(Document doc) throws IOException {
		// html解析
		//获取理财产品详细信息所在页面的url
		Elements ele1=doc.getElementsByClass("right-box");
		for(Element e1:ele1) {
			String[]content=new String[5];
			Elements ele2=e1.getElementsByAttribute("href");
			//解析出url
			String[]array=ele2.toString().split("\"");
			String str=array[1].trim();
			if(str.contains("code")) {
				int index=str.indexOf("code");
				String myurl=str.substring(index);
				String url="http://www.bankcomm.com/BankCommSite/jyjr/cn/lcpd/queryFundInfoNew.do?"+myurl;
				//System.out.println(url);
				Document d=getHTMLDoc(url);
				//System.out.println(d.toString());
				Elements ele=d.getElementsByTag("tr");
				for(Element e:ele) {
					String string=e.toString();
					//产品名称
					if(string.contains("产品名称")) {
						Elements e2=e.getElementsByTag("td");
						String []array2=e2.toString().split(">");
						String[]array3=array2[1].split("<");
						content[0]=array3[0].trim();
					}
					//产品代码
					if(string.contains("产品代码")) {
						Elements e2=e.getElementsByTag("td");
						String []array2=e2.toString().split(">");
						String[]array3=array2[1].split("<");
						content[1]=array3[0].trim();
					}
					//预计年化收益率
					if(string.contains("预计年化收益率")) {
						Elements e2=e.getElementsByTag("td");
						String []array2=e2.toString().split(">");
						String[]array3=array2[1].split("<");
						content[2]=array3[0].trim();
					}
					//起点金额
					if(string.contains("起点金额")) {
						Elements e2=e.getElementsByTag("td");
						String []array2=e2.toString().split(">");
						String[]array3=array2[1].split("<");
						content[3]=array3[0].trim();
					}
					//投资期限
					if(string.contains("投资期限")) {
						Elements e2=e.getElementsByTag("td");
						String []array2=e2.toString().split(">");
						String[]array3=array2[1].split("<");
						content[4]=array3[0].trim();
					}
					
				}
				map.put(String.valueOf(counter++), content);
				/*for(String s:content)
					System.out.println(s);
				System.out.println(counter);
				System.exit(1);*/
				
			}
			else {
				System.out.println("error");
				System.exit(1);
			}
		}
		

		
		
	}

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		BCM_Crawl crawl=new BCM_Crawl();
		//按币种筛选，美元
		String url="http://www.bankcomm.com/BankCommSite/jyjr/cn/lcpd/queryFundInfoListNew.do?currency=2&tradeType=-1&safeFlg=-1&ratio=-1&term=-1&channels=-1&asc=-undefined";
		crawl.HTMLExtract(crawl.getHTMLDoc(url));
		//按币种筛选，人民币
	    String url2="http://www.bankcomm.com/BankCommSite/jyjr/cn/lcpd/queryFundInfoListNew.do?currency=1&tradeType=-1&safeFlg=-1&ratio=-1&term=-1&channels=-1&asc=-undefined";
		crawl.HTMLExtract(crawl.getHTMLDoc(url2));
		//结果输出
		CsvWriter csvWriter = new CsvWriter("BCM_Product.csv",',', Charset.forName("GBK"));
		// 写表头
        String[] headers = {"产品名称","产品代码","预期年化收益率/业绩基准","起购金额","期限"};
        csvWriter.writeRecord(headers);
        Iterator iter=crawl.map.entrySet().iterator();
        while(iter.hasNext()) {
			Entry en=(Entry)iter.next();
			String[] content=(String[]) en.getValue();
		    csvWriter.writeRecord(content);
		}
        csvWriter.flush();
        csvWriter.close();

	}

}
