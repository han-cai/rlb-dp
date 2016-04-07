package FunctionLibrary;

import sun.nio.ch.FileChannelImpl;

import java.io.*;
import java.lang.reflect.Method;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.Charset;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.LinkedList;
import java.util.List;

public class FileOperation {

	public static String charset = "UTF-8";

	public static void setCharset(String str) {
		charset = str;
	}

	public static String toValidFileName(String uri) {
		String res = "";
		for (int i = 0; i < uri.length(); ++i) {
			char c = uri.charAt(i);
			if (c != '*' && c != '\\' && c != '/' && c != '?' && c != ':' && c != '"'
					&& c != '<' && c != '>' && c != '|')
				res += c;
		}
		return res;
	}

	public static void String2File(String filePath, String content) {
		File file = new File(filePath);
		String2File(file, content);
	}

	public static void String2File(File file, String content) {
		if (content == null)
			return;
		FileChannel write;
		try {
			write = new FileOutputStream(file).getChannel();
			write.write(ByteBuffer.wrap(content.getBytes(charset)));
			write.force(true);
			write.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static String File2String(String filePath) {
		File file = new File(filePath);
		return File2String(file);
	}

	public static String File2String(File file) {
		String content = "";
		FileChannel read;
		try {
			RandomAccessFile ranFile = new RandomAccessFile(file, "r");
			read = ranFile.getChannel();
			MappedByteBuffer inBuffer = read.map(FileChannel.MapMode.READ_ONLY, 0, read.size());
			content = ByteBuffer2String(inBuffer);

			Method m = FileChannelImpl.class.getDeclaredMethod("unmap", MappedByteBuffer.class);
			m.setAccessible(true);
			m.invoke(FileChannelImpl.class, inBuffer);
			read.close();
			ranFile.close();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		return content;
	}

	public static String ByteBuffer2String(ByteBuffer buffer) {

		CharBuffer charBuffer = null;
		Charset cset = Charset.forName(charset);
		charBuffer = cset.decode(buffer);
		buffer.flip();
		return charBuffer.toString();


	}

	public static void Add2File(File file, String content) {
		if (content == null)
			return;
		FileChannel write;
		try {
			write = new RandomAccessFile(file, "rw").getChannel();
			write.position(write.size());
			write.write(ByteBuffer.wrap(content.getBytes(charset)));
			write.force(true);
			write.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static void Add2File(String filePath, String content) {
		File file = new File(filePath);
		Add2File(file, content);
	}

	public static void DeleteFile(String filePath) {
		File toDelete = new File(filePath);
		if (toDelete.isDirectory()) {
			File[] childs = toDelete.listFiles();
			for (File child : childs) {
				DeleteFile(child.getAbsolutePath());
			}
		}
		toDelete.delete();
	}

	public static String GetPureFileName(String str) {
		int index = str.lastIndexOf(".");
		if (index < 0 || index >= str.length()) return null;
		return str.substring(0, index);
	}

	public static List<File> GetFileList(File dir) {
		List<File> fileList = new LinkedList<File>();
		if (dir.isFile()) {
			fileList.add(dir);
		} else {
			try {
				DirectoryStream<Path> stream = Files.newDirectoryStream(Paths.get(dir.getAbsolutePath()));
				for (Path entry : stream) {
					File file = entry.toFile();
					if (file.isFile()) {
						fileList.add(file);
					} else {
						fileList.addAll(GetFileList(file));
					}
				}
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		return fileList;
	}

	public static void AddLog(String filePath, String log){
		Add2File(filePath, log + "\n");
	}

	public static void AddLog(File file, String log){
		Add2File(file, log + "\n");
	}
}
