import java.math.RoundingMode;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

import javax.swing.plaf.synth.SynthSeparatorUI;

/**
 * 
 */

/**
 * @author Moncada
 *
 */
public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) {

		//test1();
		//test2();
		//for (int i = 0; i< 10; i++)
		//	test3();
		uniformQuaternions();

	}
	
	public static void uniformQuaternions(){
		int numberQuat = 6600;
		int numberOfRandoms = 100;
		quaternionsOperations op = new quaternionsOperations();
		List<double[]> points = generatePoints();
		
		ArrayList <Quaternion> quatGroup = new  ArrayList<Quaternion>(numberQuat);
		
		//adicionar o primeiro
		quatGroup.add(op.generateRandomQ());
		long initialTime = System.currentTimeMillis();
		
		Quaternion quatToAdd = null;
		for (int i = 0; i< numberQuat; i++){
			double maxDistQuat = 0;
			
			for (int j = 0; j<numberOfRandoms; j++){
				double minOfQuat = Double.MAX_VALUE;
				//gerar o quat aleatorio
				Quaternion r = op.generateRandomQ();
				//percorrer todos e ver o que est� mais perto
				for (Quaternion q: quatGroup){
					double dist = calculateDist(q,r, points);
					
					if (dist < minOfQuat)
						minOfQuat = dist;
				}
				//dos mais pertos, agarrar o que est� mais longe
				if (minOfQuat > maxDistQuat){
					maxDistQuat = minOfQuat;
					quatToAdd = r;
				}	
			}
			
			
		quatGroup.add(quatToAdd);		
		}
		
		long finalTime = System.currentTimeMillis();
		System.out.println("Total time: " + (finalTime - initialTime));
		
		//for (Quaternion q: quatGroup){
		//	System.out.println(q.toString());
		//}
	}
	
	public static List<double[]> generatePoints(){
		List<double[]> points = new ArrayList<double[]>();
		double [] point =  new double [3];
		
		point[0] = 0;
		point[1] = 0;
		point[2] = 0;
		points.add(point);
		
		point[0] = 3;
		point[1] = 3;
		point[2] = 3;
		points.add(point);
		
		point[0] = 3;
		point[1] = 3;
		point[2] = 0;
		points.add(point);
		
		point[0] = 3;
		point[1] = 0;
		point[2] = 0;
		points.add(point);
		
		point[0] = 0;
		point[1] = 3;
		point[2] = 0;
		points.add(point);
		
		point[0] = 0;
		point[1] = 0;
		point[2] = 3;
		points.add(point);
		
		point[0] = 0;
		point[1] = 3;
		point[2] = 3;
		points.add(point);
		
		point[0] = 3;
		point[1] = 0;
		point[2] = 3;
		points.add(point);
		
		return points;
	}
	
	//returna a distancia entre dois quaterni�es baseando-se num conjunto de pontos.
	public static double calculateDist(Quaternion q, Quaternion r, List<double []> points){
		double maxDist = 0;
		quaternionsOperations op = new quaternionsOperations();
		for (double [] c: points){
			Quaternion q1 = op.timesWithVector(q, c);
			Quaternion q2 = op.timesWithVector(r, c);
			double [] point1 = q1.getPoint();
			double [] point2 = q2.getPoint();
			double distancia3D = Math.sqrt( Math.pow( (point1[0] - point2[0]),2 ) + Math.pow( (point1[1] - point2[2]),2 ) +  Math.pow( (point1[2] - point2[2]),2 )) ;
			if( Math.abs(distancia3D) > maxDist)
				maxDist = distancia3D;
		}
		return maxDist;
	}
		
	//testa a rota��o de um point nos 3 eixos (um de cada vez) por 360 graus
 	public static void test1(){
		quaternionsOperations op = new quaternionsOperations();
		// ponto de teste, em formato quaternion
		double [] point = new double[3];
		point[0] = 1;
		point[1] = 1;
		point[2] = 1;
		double angle = 360;
		
		//primeiro vetor
		double [] vetor = new double[3];
		vetor[0] = 1;
		vetor[1] = 0;
		vetor[2] = 0;
		
		Quaternion q0 = op.CalcQuaternion(point, vetor, angle);
		
		//point[0] = q0.getX1();
		//point[1] = q0.getX2();
		//point[2] = q0.getX3();
		
		point = q0.getPoint();
		
		//segundo vetor
		vetor[0] = 0;
		vetor[1] = 1;
		vetor[2] = 0;
		Quaternion q1 = op.CalcQuaternion(point, vetor, angle);
		
		//point[0] = q1.getX1();
		//point[1] = q1.getX2();
		//point[2] = q1.getX3();
		
		point = q1.getPoint();
		//segundo vetor
		vetor[0] = 0;
		vetor[1] = 1;
		vetor[2] = 0;
		Quaternion q2 = op.CalcQuaternion(point, vetor, angle);
		
		System.out.println(q2.toString());
	}
	
	//testa a rota��o de um point nos 3 eixos por 360 graus
	public static void test2(){
		quaternionsOperations op = new quaternionsOperations();
		//ponto de teste
		double [] point = new double[3];
		point[0] = 1;
		point[1] = 0;
		point[2] = 0;
		double angle = 120;
		
		//primeiro vetor
		double [] vetor = new double[3];
		vetor[0] = 1;
		vetor[1] = 1;
		vetor[2] = 1;
		
		Quaternion q0 = op.CalcQuaternion(point, vetor, angle);
		
		System.out.println(q0.toString());
	}

	public static void test3(){
		quaternionsOperations op = new quaternionsOperations();
		
		Quaternion q = op.generateRandomQ();
		System.out.println(q.toString());
	}
}
