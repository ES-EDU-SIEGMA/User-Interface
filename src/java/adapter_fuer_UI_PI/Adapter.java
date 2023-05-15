


public class Adapter implements UserInterfaceListner {
	
	private Terminal terminal;
	private GUI gui;
	
	public void readDrinkNumber() {
		terminal = new Terminal();
		terminal.readDrinkNumber();
	}
	
	public  void pressendButton(){
		}
			
	public void showWindow() {
		gui = new GUI();
		gui.showWindow();
		
	}
	
}
