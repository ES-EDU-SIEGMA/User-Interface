



public class Client {
	
	public static void main(String args[]){
		String arg = null;
		
		if(args.length > 0) {
			arg = args[0];
			if(arg.equals("gui")){
				UserInterfaceListner uiListner = new Adapter();
				uiListner.showWindow();
			}
			else
				System.out.println("Wat? Mit solchen Argumenten verkehre ich nicht :-/");
		}
		else {
			UserInterfaceListner uiListner = new Adapter();
			uiListner.readDrinkNumber();
		}

	}

}

