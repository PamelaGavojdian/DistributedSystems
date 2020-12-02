import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.util.Arrays;
import java.util.List;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class MessengerWithFiles {
	
	public static void main(String[] CLA) 
	{
		List<String> args = Arrays.asList(CLA); 


		boolean hasL = args.contains("-l"); // program has to start with this option because its the socket its server will listen to 
		boolean hasS = args.contains("-s"); // specifies the address of the server to connect to 
		boolean hasP = args.contains("-p"); // specifies the port number of the server to connect to 

		boolean isServer = false;



		int serverPort = 0; // initialize the server port number
		int lPort = 0;  // initialize the Listening Port Number

		String address = "localhost";

		// check and see if -l is present. 
		if (!hasL) { 
			System.out.println("Error ");
			System.exit(0);
		}

		// create a listening port called lPort 
		lPort = Integer.valueOf(args.get(args.indexOf("-l") + 1));


		// if there is a port number or adress of the server then Run as the Client
		if (hasS || hasP) 
		{ 
			if (hasP)
				serverPort = Integer.valueOf(args.get(args.indexOf("-p") + 1));

			if (hasS)
				address = args.get(args.indexOf("-s") + 1);
		} else
			isServer = true;

		if (isServer)
			startServer(lPort);
		else
			startClient(lPort, serverPort);

	}

	public static class Options implements Runnable {
		private int lPort; // listening port 
		private DataOutputStream output; // output 
		

		public Options(DataOutputStream output, int lPort) 
		{
			this.output = output;
			this.lPort = lPort;
		}

		@Override
		public void run() {
			try {

				// initialize scanner 
				Scanner in = new Scanner(System.in);

				// create placehold for the user input 
				String choice = ""; 

				// Exit the loop 
				boolean exit = false; 
				

				// create a while loop that says if the user 
				// entered information and  the loop did not exit 
				while (choice != null && !exit) 
				{

					// Prompt the user to enter a choice of either m, f, or x 
					// the m stands for send a message
					// the f stands for request file
					// the x exits the program and disconnects from the other messenger


					System.out.println("Enter an option ('m', 'f', 'x'):\n" + "  (M)essage (send)\n"
							+ "  (F)ile (request)\n" + " e(X)it"); 

					// store the information from the user in choice. 
					choice = in.nextLine();

					switch (choice) 
					{
					
					// if the user enters "m" then they want to send a message. 
					case "m": 
						// send message to the user
						System.out.println("Enter your message:");
						// once user enters value then store it in message 
						String message = in.nextLine();

						output.writeUTF(message);
						break;




					// prompts the user to enter the file they want 
					case "f": 
						//send message to the user 
						System.out.println("Which file do you want?");
						//once the user enters value store it into File Name 
						String fName = in.nextLine();
						// create new File Transfer
						FileTransfer fileTransfer = new FileTransfer(fName, lPort);
						Thread fileTransferThread = new Thread(fileTransfer);
						// start the file transfer
						fileTransferThread.start();
						break;

					// as soon as the user enters "X" connections end and terminate 	
					case "x": 
						exit = true;
						break;
					default:
						System.out.println("closing your sockets... goodbye");
					}
				}
				
				// close and end the server.
				in.close();
				output.writeUTF(""); 
			} catch (Exception e) {
				System.exit(1);
			}
		}
	}
	
	public static class FileTransfer implements Runnable {
		private String fName; // File Name 
		private int lPort; // listening Port 

		public FileTransfer(String fName, int lPort) {
			this.lPort = lPort; // listening Port 
			this.fName = fName; // File Name 
			
		}

		@Override
		public void run() {
			try {

				//create new client socket 
				Socket clientSocket = new Socket("localhost", lPort);
				// initizalize the output 
				DataOutputStream output = new DataOutputStream(clientSocket.getOutputStream());

				//initizalize the input 
				DataInputStream input = new DataInputStream(clientSocket.getInputStream());

				output.writeUTF(fName);
				FileOutputStream fOut = new FileOutputStream(fName);

				// create a integer called number_read
				int number_read;
				byte[] buffer = new byte[1500];
				while ((number_read = input.read(buffer)) != -1)
					fOut.write(buffer, 0, number_read);
				//close 
				fOut.close(); 
				clientSocket.close();
			} catch (Exception e) {
				System.exit(2);
			}

		}
	}
	// class that the client recieved from the server 
	// that is server send to the client 

	
	public static class ReceiveClient implements Runnable { 
		int lPort; // initizalize the listening port 

		public ReceiveClient(int lPort) {
			this.lPort = lPort; // listening Port 
		}

		@Override
		public void run() {
			try {
				
				ServerSocket serverSocket = new ServerSocket(lPort);

				// loop that continues as long as its true. if its false it terminates 
				while (true) 
				{
					int number_read;
					Socket clientSocket = serverSocket.accept();


					DataOutputStream output = new DataOutputStream(clientSocket.getOutputStream());
					DataInputStream input = new DataInputStream(clientSocket.getInputStream());


					String fName = input.readUTF();

					// create a new file called file from the fName 
					File file = new File(fName);

					FileInputStream fInput = new FileInputStream(file);

					byte[] buffer = new byte[1500];


					while ((number_read = fInput.read(buffer)) != -1)
						output.write(buffer, 0, number_read);
					//close
					fInput.close();
					clientSocket.close();
				}
			} catch (Exception e) {
				System.exit(3);
			}

		}
	}
	
	public static class ReceiveServer implements Runnable{
		ServerSocket serverSocket;
		
		public ReceiveServer(ServerSocket serverSocket) {
			this.serverSocket = serverSocket;
		}
		
		@Override
		public void run() {
			try {
				while(true) 
				{
					int number_read;
					// create a new socket called clientSocket 
					Socket clientSocket = serverSocket.accept();
					// initialize the DataOuput Stream output where the output is stored
					DataOutputStream output = new DataOutputStream(clientSocket.getOutputStream());
					// initialize the DataInput Stream input where the input is stored. 
					DataInputStream input = new DataInputStream(clientSocket.getInputStream());

					String fName = input.readUTF();


					File file = new File(fName);
					FileInputStream fInput = new FileInputStream(file);
					byte[] buffer = new byte[1500];

					
					while ((number_read = fInput.read(buffer)) != -1)
						output.write(buffer, 0, number_read);
					//close 
					fInput.close();
					clientSocket.close();
				}
			} catch (Exception e) {
				System.exit(4);
			}
		}
	}


	
	private static void startServer(int port) {
		try {
		
			// initizalise the server socket called ServerSocket to handle the server. 
			ServerSocket serverSocket= new ServerSocket(port);

			// initialize the client socket called clientSocket to handle the client. 
			Socket clientSocket= serverSocket.accept();
			


			//responsible for the output 
			DataOutputStream output= new DataOutputStream(clientSocket.getOutputStream());
			// responsible for the input 
			DataInputStream input= new DataInputStream(clientSocket.getInputStream());
			

			// listening port string
			String lPortString = input.readUTF(); 
			// listening port integer value 
			int lPort = Integer.valueOf(lPortString);
			
			ReceiveServer receive = new ReceiveServer(serverSocket);
			Options options = new Options(output, lPort);

			// create new thread called recieveThread
			Thread receiveThread = new Thread(receive);
			// create new thread called optionsThread
			Thread optionsThread = new Thread(options);
			
			// start both the reiceved thread and options thread
			receiveThread.start();
			optionsThread.start();
			

			String message = "";

			while ((message = input.readUTF()) != null) {
				if (message.length() == 0) {
					break;
				} else {
					System.out.println(message);
				}

			}
			output.writeUTF("");
			// close the server socket, slient socket, shut down and exit 
			serverSocket.close();
			clientSocket.shutdownOutput();
			clientSocket.close();
			System.exit(0);
		} catch (Exception e) {
			System.exit(5);
		}
	}

	private static void startClient(int lPort, int serverPort) {
		try {
			Socket clientSocket = new Socket("localhost", serverPort);
			DataOutputStream output = new DataOutputStream(clientSocket.getOutputStream());
			DataInputStream input = new DataInputStream(clientSocket.getInputStream());
			output.writeUTF(Integer.toString(lPort));
			
			ReceiveClient receive = new ReceiveClient(lPort);
			Options options = new Options(output, serverPort);

			// create recieved thread 
			Thread receiveThread = new Thread(receive);
			//create options thread 
			Thread optionsThread = new Thread(options);
			
			// start the options thread and recieve thread
			optionsThread.start();
			receiveThread.start();
			

			String message = "";


			while ((message = input.readUTF()) != null) {
				if (message.length() == 0) {
					break; // exits 
				} else {
					// print out what is stored in message 
					System.out.println(message);
				}

			}
			output.writeUTF("");
			//close the client socket and exit
			clientSocket.close();
			System.exit(0);

			// terminate when there is an error
		} catch (Exception e) {
			System.exit(6);
		}

	}
}