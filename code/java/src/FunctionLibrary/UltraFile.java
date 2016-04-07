package FunctionLibrary;

import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;

public class UltraFile {

	public enum WriteOption {
		ADD, WRITE
	}
	public String charset;

	public File file;
	public FileChannel writer;
	public BufferedReader reader;

	public int windowSize;
	public int counter;
	public long stime;

	public UltraFile(String filePath, int windowSize) {
		file = new File(filePath);
		writer = null;
		reader = null;
		this.windowSize = windowSize;
		counter = 0;
		charset = "UTF-8";
	}


	public UltraFile(String filePath) {
		file = new File(filePath);
		writer = null;
		reader = null;
		this.windowSize = 1000000;
		counter = 0;
		charset = "UTF-8";
	}

	public void setCharset(String str) {
		charset = str;
	}

	public String readLine() throws Exception {
		if (reader == null) {
			reader = new BufferedReader(new InputStreamReader(new FileInputStream(file), charset));
			stime = System.currentTimeMillis();
		}
		String line = reader.readLine();
		if (line == null) {
			//System.out.println("Reading Finish: " + counter + "\t" + file.getAbsolutePath());
		} else {
			counter++;
			if (counter % windowSize == 0) {
				long etime = System.currentTimeMillis();
				System.out.println("Read " + windowSize + ":\t" + (etime - stime));
				stime = etime;
			}
		}
		return line;
	}

	public void initWriter(WriteOption option) throws Exception {
		switch (option) {
			case ADD:
				writer = new RandomAccessFile(file, "rw").getChannel();
				writer.position(writer.size());
				break;
			case WRITE:
				writer = new FileOutputStream(file).getChannel();
				break;
			default:
		}
		counter = 0;
		stime = System.currentTimeMillis();
	}

	public void write(String str) throws Exception {
		writer.write(ByteBuffer.wrap(str.getBytes(charset)));
	}

	public void writeLine(String str) throws Exception {
		write(str + "\n");
		counter++;
		if (counter % windowSize == 0) {
			long etime = System.currentTimeMillis();
			System.out.println("Write " + windowSize + ":\t" + (etime - stime));
			stime = etime;
		}
	}

	public void close() throws Exception {
		if (reader != null) {
			reader.close();
			reader = null;
		}
		if (writer != null) {
			writer.force(true);
			writer.close();
			writer = null;
		}

	}
}
