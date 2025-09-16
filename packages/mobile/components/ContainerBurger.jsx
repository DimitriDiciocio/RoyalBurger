import React from 'react';
import { View, StyleSheet, Image } from 'react-native';

export default function ContainerBurger({ }) {
  return (
    <View style={styles.container}>
      <View style={styles.imageWrapper}>
        <Image
          style={styles.image}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: 120,
    height: 160,
    backgroundColor: '#fff',
    borderRadius: 10
  },
  imageWrapper: {
    width: 120,
    height: 85,
    backgroundColor: '#D9D9D9',
    borderRadius: 10
  },
  image: {
    width: 120,
    height: 85,
  },
});