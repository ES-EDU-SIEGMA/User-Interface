
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;

public class GUI {
	
	public void showWindow() {
		System.out.println("gui");
		JFrame frame = new JFrame("Getränkeauswahl");
		
		JPanel panel = new JPanel();
		JButton button1 = new JButton("Spezi");
		JButton button2 = new JButton("Super-Spezi");
		JButton button3 = new JButton("H20");
		
		button1.addActionListener(e -> {
			System.out.println("Auwahlahl ist 1: Spezi");
		});
		
		button2.addActionListener(e -> {
			System.out.println("Auswahl ist 2: Super-Spezi");
		});
			
		button3.addActionListener(e -> {
			System.out.println("Auswahl ist 3: H20");
		});
		
		panel.add(button1);
		panel.add(button2);
		panel.add(button3);
		
		frame.getContentPane().add(panel);
	
		frame.setSize(300,200);
		frame.setVisible(true);
			
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}
}
